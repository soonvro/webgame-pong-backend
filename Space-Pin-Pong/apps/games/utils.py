import math
import numpy


def distance_line_point(line: tuple[int, int, int, int], p: tuple[int, int]) -> float:
    """
    선분과 점 사이의 거리를 구하는 함수입니다.
    parameters:
        line: (s_x, s_y, e_x, e_y) 형태의 선분 좌표
        point: (p_x, p_y) 형태의 점 좌표
    """
    s_x, s_y, e_x, e_y = line
    p_x, p_y = p
    # 선분의 길이
    line_length = math.hypot(e_x - s_x, e_y - s_y)
    if line_length == 0:
        return math.hypot(p_x - s_x, p_y - s_y)

    # 방향 벡터들
    se_vec = numpy.array([e_x - s_x, e_y - s_y])
    sp_vec = numpy.array([p_x - s_x, p_y - s_y])
    es_vec = numpy.array([s_x - e_x, s_y - e_y])
    ep_vec = numpy.array([p_x - e_x, p_y - e_y])

    # 점의 수선의 발이 선분 위에 있는 경우
    if numpy.dot(se_vec, sp_vec) <= 0 or numpy.dot(es_vec, ep_vec) <= 0:
        return float(numpy.cross(se_vec, sp_vec) / line_length)

    # 점의 수선의 발이 선분 위에 없는 경우
    return min(float(numpy.linalg.norm(sp_vec)), float(numpy.linalg.norm(ep_vec)))