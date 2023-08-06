import numpy
from scipy.spatial import ConvexHull

my_epsilon = 1e-6

def hullends(points:numpy.ndarray):
    """给一串链先计算hull，再给hull添加两个端点，返回端点的坐标。"""
    hull = ConvexHull(points)
    N_points = points.shape[0]
    N_plane = hull.equations.shape[0]
    # 计算质心坐标
    center = numpy.zeros(3)
    for i in range(N_points):
        center += points[i]
    center /= N_points

    # 计算末端距离
    dis_end_end = numpy.linalg.norm(points[0]-points[-1])

    # 计算points[0]和points[-1]到所有平面的距离，并且提取最小的平面
    min_distance_0 = 1e10
    min_index_0 = 0   
    min_distance_1 = 1e10
    min_index_1 = 0

    for i in range(N_plane):
        distance = abs(numpy.dot(hull.equations[i][0:3], points[0]) + hull.equations[i][3])
        if distance < min_distance_0:
            min_distance_0 = distance
            min_index_0 = i
        distance = abs(numpy.dot(hull.equations[i][0:3], points[-1]) + hull.equations[i][3])
        if distance < min_distance_1:
            min_distance_1 = distance
            min_index_1 = i

    vec0 = numpy.zeros(3)
    vec1 = numpy.zeros(3)
    # 如果端点在凸包平面上，vec0 选择为从center指向中心points[0]
    if(min_distance_0<my_epsilon):
        vec0 = points[0] - center
    
    else:
        # 否则，vec0选择为points[0]距离最近的平面的法向量，向量模为min_distance_0
        vec0 = hull.equations[min_index_0][0:3]
        vec0 /= numpy.linalg.norm(vec0)
        vec0 *= min_distance_0

    if(min_distance_1<my_epsilon):
        vec1 = points[-1] - center
    else:
        vec1 = hull.equations[min_index_1][0:3]
        vec1 /= numpy.linalg.norm(vec1)
        vec1 *= min_distance_1

    # rescale 来确保新加的两个点比较远

    # 计算xyz三个方向上的最大距离
    max_distance = 0
    for i in range(N_points):
        for j in range(i+1, N_points):
            distance = numpy.linalg.norm(points[i]-points[j])
            if distance > max_distance:
                max_distance = distance

    # 计算vec0和vec1的xyz三个方向上的最小值
    min_vec0 = 1e10
    min_vec1 = 1e10
    for i in range(3):
        if abs(vec0[i]) < min_vec0:
            min_vec0 = abs(vec0[i])
        if abs(vec1[i]) < min_vec1:
            min_vec1 = abs(vec1[i])
    # rescale0和rescale1分别是vec0和vec1的缩放比例, 用max_distance/min_vec0 
    # 
    rescale0 = max_distance/min_vec0
    rescale1 = max_distance/min_vec1

    # 计算两个返回点
    p0 = points[0] + vec0*rescale0
    p1 = points[-1] + vec1*rescale1

    return p0, p1


def cal_normals(p1, p2, p3, plain):
    """Calculate the normal vector of a plane."""
    v1 = p2 - p1
    v2 = p3 - p1
    v3 = numpy.cross(v1, v2)
    # 法向量的模保存为v3_norm
    v3_norm = numpy.linalg.norm(v3)
    
    if(v3_norm<my_epsilon):
        # 如果法向量的模小于my_epsilon，说明三个点共线，直接返回
        return
    
    plain[0:3]=v3/v3_norm
    plain[3]=0
    plain[3]-=numpy.dot(plain[0:3], p1)
    return plain

def judge_triangle(p1:numpy.ndarray, p2:numpy.ndarray, p3, plain, p4, p5):
    """p1,p2,p3三个点组成的三角形,如果p4-p5的向量穿过三角形,返回1,Otherwise,return 0."""
    # 计算p4，p5到平面的距离
    d1 = numpy.dot(plain[0:3], p4) + plain[3]
    d2 = numpy.dot(plain[0:3], p5) + plain[3]
    # 如果两个点在平面的同一侧，说明p4-p5不穿过三角形
    if d1*d2 > 0:
        return 0
    # 如果两个点在平面内，返回1
    if abs(d1)<my_epsilon and abs(d2)<my_epsilon:
        return 1

    # 计算p4-p5的向量和三角形的所在平面的交点
    # 用E1,E2,E3表示三角形的三个边
    E1 = p2 - p1
    E2 = p3 - p1

    # T表示p4-p1的向量
    T = p4 - p1
    d = p5 - p4

    # 计算各个参数
    M = numpy.cross(d, E2)
    det = numpy.dot(E1, M)
    K = numpy.cross(T, E1)
    t = numpy.dot(K, E2)/det
    u = numpy.dot(M, T)/det
    v = numpy.dot(K, d)/det
    if u < 0 or v < 0 or u + v > 1 or t > 1 or t < 0:
        return 0
    # print(det, u, v, t)
    return 1


def KMT_open(points:numpy.ndarray):
    """Simplify conformation of open chains by KMT algorithm."""
    flag = 0

    while True:
        number = points.shape[0]# 作为判断是否结束循环的标志，当没有vertex可以删除的时候，就退出。
        # if(number<8):
        #     break

        i=0
        while True:
            i+=1
            # print(i, '\t', len(points))
            plain = numpy.zeros(4)
            flag = 0
            if ((i+1)>=len(points)):
                break
            cal_normals(points[i-1], points[i], points[(i+1)], plain)

            if abs(plain[0]) < my_epsilon and abs(plain[1]) < my_epsilon and abs(plain[2]) < my_epsilon:
                # 如果三个点在一条线上，可以省去,从numpy数组中删除这个点
                points = numpy.delete(points, i, axis=0)
                i -= 1
                # print(i)
                # print(len(points))
                continue

            for j in range(len(points)-1):
                if j == i-1 or j == i or j==i+1:
                    continue
                if judge_triangle(points[i-1], points[i], points[(i+1)], plain, points[j], points[(j+1)])==1:
                    flag = 1
                    break

            if flag == 0:
                points = numpy.delete(points, i, axis=0)  
                i -= 1
                # print(i)
                # print(len(points))

        if number == len(points):
            break
    #print(len(points))
    return points

def KMT_open_n_times(points:numpy.ndarray,n):
    """Simplify conformation of open chains by KMT algorithm, only compare with n times."""
    flag = 0

    for k in range(n):
        number = points.shape[0]# 作为判断是否结束循环的标志，当没有vertex可以删除的时候，就退出。
        # if(number<8):
        #     break

        i=0
        while True:
            i+=1
            # print(i, '\t', len(points))
            plain = numpy.zeros(4)
            flag = 0
            if ((i+1)>=len(points)):
                break
            cal_normals(points[i-1], points[i], points[(i+1)], plain)

            if abs(plain[0]) < my_epsilon and abs(plain[1]) < my_epsilon and abs(plain[2]) < my_epsilon:
                # 如果三个点在一条线上，可以省去,从numpy数组中删除这个点
                points = numpy.delete(points, i, axis=0)
                i -= 1
                # print(i)
                # print(len(points))
                continue

            for j in range(len(points)-1):
                if j == i-1 or j == i :
                    continue
                if judge_triangle(points[i-1], points[i], points[(i+1)], plain, points[j], points[(j+1)])==1:
                    flag = 1
                    break

            if flag == 0:
                points = numpy.delete(points, i, axis=0)  
                i -= 1
                # print(i)
                # print(len(points))

        if number == len(points):
            break
    #print(len(points))
    return points

def find_max_span(points:numpy.ndarray):
    """Find the maximum span of the points, and translate to the max span"""
    max_span = 0
    for i in range(len(points)-1):
        for j in range(i+1, len(points)):
            span = numpy.linalg.norm(points[i]-points[j])
            if span > max_span:
                max_span = span
    return max_span