from edge import *
from point import *

class ScanLineAlgoritm():

    @classmethod
    def __get_active_polygons(cls, polygons):
        "Remove from polygons sequence items without 2D representation."
        return [p for p in polygons if all([e.is_representation2D() for e in p.edges])]

    @classmethod
    def __get_edges_y_range(cls, polygons):
        "Calculate minimum and maximum of sequence of edges on axis y."
        r_min = min([e.edge2D.get_axis_param('y', min) for p in polygons for e in p.edges])
        r_max = max([e.edge2D.get_axis_param('y', max) for p in polygons for e in p.edges])

        return (int(r_min), int(r_max))

    @classmethod
    def __get_y_const2D_edges_dict(cls, polygons, y_range, throwing_area):
        "Get dictionary of edges with edge2D type Y_CONST."

        def get_cross_with_y_axis_2D(polygon, y):
            cross2D = [(e, e.edge2D.cross_with_axis('y', y)) for e in polygon.edges]
            cross2D = list(filter(lambda c: c[1], cross2D))
            
            return cross2D

        def get_cross3D(cross2D):
            cross3D = []
            for c in cross2D:
                if(type(c[1]) == tuple):
                    cross3D.extend((c[0].edge3D.s_point, c[0].edge3D.e_point))
                else:
                    t = c[0].edge3D.get_transformation_ratio(c[1], throwing_area)
                    cross3D.append(c[0].edge3D.get_point(t))
            cross3D.sort(key=lambda c: c.x)

            return cross3D

        def get_y_const2D_edges(polygon, y):
            edges = []
            cross2D = get_cross_with_y_axis_2D(polygon, y)
            cross3D = get_cross3D(cross2D)
            for i in range(0, len(cross3D)-1, 2):
                try:
                    edge = Edge((cross3D[i], cross3D[i+1]), throwing_area, polygon.color)
                    edges.append(edge)
                except (PointException, EdgeException):
                    pass

            return edges

        edges_dict = {}
        for y in range(y_range[0], y_range[1]+1):
            for p in polygons:
                edges = get_y_const2D_edges(p ,y)
                edges_dict.setdefault(y, []).extend(edges)
        
        return edges_dict

    @classmethod
    def __get_y_const2D_subedges_dict(cls, edges_dict, throwing_area):
        
        def subcross_with_edge2D_init(edges):
            return [[e, e.edge2D.s_point, e.edge2D.e_point] for e in edges]
            
        def get_subcross_with_edge2D(edges):
            subcross2D = subcross_with_edge2D_init(edges)
            for i in range(0, len(edges)-1):
                for j in range(i+1, len(edges)):
                    cross2D = edges[i].edge2D.cross_with_edge(edges[j].edge2D)
                    if(cross2D):
                        if(type(cross2D) == tuple):
                            list(map(lambda c: subcross2D[i].append(c), [c for c in cross2D if c not in subcross2D[i]]))
                            list(map(lambda c: subcross2D[j].append(c), [c for c in cross2D if c not in subcross2D[j]]))
                        else:
                            if(cross2D not in subcross2D[i]): subcross2D[i].append(cross2D)
                            if(cross2D not in subcross2D[j]): subcross2D[j].append(cross2D)

            for i, sc in enumerate(subcross2D[:]):
                subcross2D[i][1:] = sorted(sc[1:], key = lambda p2D: p2D.x)
            
            return subcross2D

        def get_subcross3D(subcross2D):
            subcross3D = [[sc[0]] for sc in subcross2D]
            for i, sc in enumerate(subcross2D):
                for p2D in sc[1:]:
                    t = sc[0].edge3D.get_transformation_ratio(p2D, throwing_area)
                    if(type(t) == tuple):
                        pass
                        # subcross3D[i].append(sc[0].edge3D.get_point(-1))
                        # subcross3D[i].append(sc[0].edge3D.get_point(1))
                    else:    
                        subcross3D[i].append(sc[0].edge3D.get_point(t))

            return subcross3D

        def get_y_const2D_subedges(subcross3D):
            subedges = []
            for sc in subcross3D:
                for i in range(1, len(sc)-1):
                    try:
                        points3D = (sc[i], sc[i+1])
                        subedges.append(Edge(points3D, throwing_area, sc[0].color))
                    except (PointException, EdgeException):
                        pass

            subedges.sort(key=lambda se: se.edge3D.get_axis_param('z', min), reverse=True)

            return [se.edge2D for se in subedges]

        subedges_dict = {}
        for y, edges in edges_dict.items():
            subcross2D = get_subcross_with_edge2D(edges)
            subcross3D = get_subcross3D(subcross2D)
            subedges = get_y_const2D_subedges(subcross3D)
            subedges_dict[y] = subedges
        
        return subedges_dict

    @classmethod
    def scan(cls, polygons, throwing_area):
        active_polygons = cls.__get_active_polygons(polygons)
        if(active_polygons):
            y_range = cls.__get_edges_y_range(active_polygons)
            y_const2D_edges_dict = cls.__get_y_const2D_edges_dict(active_polygons, y_range, throwing_area)
            y_const2D_subedges_dict = cls.__get_y_const2D_subedges_dict(y_const2D_edges_dict, throwing_area)
            return y_const2D_subedges_dict
        else:
            return []