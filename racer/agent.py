
import math
import point


class Agent(object):

    def __init__(self, model_x, model_y):
        self.model_x = model_x
        self.model_y = model_y
        self.delta_t = 0.1
        self.k = 3

    def get_normal_dist(self, X, std):
        coeff = 1.0 / (std * math.sqrt(2 * math.pi))
        return coeff * math.exp(- math.pow(X, 2) / (2.0 * math.pow(std, 2)))

    def get_position(self, t_0):
        return point.Point(self.model_x(t_0), self.model_y(t_0))

    def get_probability(self, x, y, t_0, t_m):
        # t_0 is the current time, don't fuck this up
        assert t_0 < t_m
        t = t_0
        prob_sum = 0.0
        num_samples = (t_m - t_0) / self.delta_t

        while t < t_m:
            pos = self.get_position(t)
            dist = pos.dist_to(point.Point(x, y))
            prob = self.get_normal_dist(dist, self.k * (t - t_0) + 1)
            prob_sum += prob
            t += self.delta_t

        return prob_sum / num_samples

    def get_pdf(self, t_0, t_m):
        assert t_0 < t_m
        return lambda x, y: self.get_probability(x, y, t_0, t_m)


def get_probability(x, y, t_0, t_m, *agents):
    assert len(agents) > 0
    assert t_0 < t_m
    sum_prob = 0.0
    for a in agents:
        sum_prob += a.get_probability(x, y, t_0, t_m)

    return sum_prob / len(agents)


def get_pdf(t_0, t_m, *agents):
    assert len(agents) > 0
    assert t_0 < t_m
    a_list = list()
    for a in agents:
        a_list.append(a.get_pdf(t_0, t_m))

    def __get_pdf(x, y):
        sum_prob = 0.0
        for pdf in a_list:
            sum_prob += pdf(x, y)

        return sum_prob / len(agents)

    return __get_pdf
