import ball
import my_event
import turtle
import random
import heapq
import seven_segments_proc


class BouncingSimulator:
    def __init__(self, _num_balls):
        self.num_balls = _num_balls
        self.ball_list = []
        self.t = 0.0
        self.pq = []
        self.HZ = 4
        turtle.speed(0)
        turtle.tracer(0)
        turtle.hideturtle()
        turtle.colormode(255)
        self.canvas_width = turtle.screensize()[0]
        self.canvas_height = turtle.screensize()[1]
        print(self.canvas_width, self.canvas_height)

        ball_radius = 0.05 * self.canvas_width
        for i in range(self.num_balls):
            x = -self.canvas_width + (i + 1) * (2 * self.canvas_width / (self.num_balls + 1))
            y = 0.0
            vx = 10 * random.uniform(-1.0, 1.0)
            vy = 10 * random.uniform(-1.0, 1.0)
            ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, i))

        for k in range(0,10):
            tom = turtle.Turtle()
            self.my_number = seven_segments_proc.Number(200, 50, (255, 0, 0), tom, k)
            self.my_number.set_location([0, -50])
            self.screen = turtle.Screen()

    # updates priority queue with all new events for a_ball
    def __predict(self, a_ball):
        if a_ball is None:
            return

        # particle-particle collisions
        for i in range(len(self.ball_list)):
            dt = a_ball.time_to_hit(self.ball_list[i])
            # insert this event into pq
            heapq.heappush(self.pq, my_event.Event(self.t + dt, a_ball, self.ball_list[i]))

        # particle-wall collisions
        dtX = a_ball.time_to_hit_vertical_wall()
        dtY = a_ball.time_to_hit_horizontal_wall()
        heapq.heappush(self.pq, my_event.Event(self.t + dtX, a_ball, None))
        heapq.heappush(self.pq, my_event.Event(self.t + dtY, None, a_ball))

    def __draw_border(self):
        turtle.penup()
        turtle.goto(-self.canvas_width, -self.canvas_height)
        turtle.pensize(10)
        turtle.pendown()
        turtle.color((0, 0, 0))
        for i in range(2):
            turtle.forward(2 * self.canvas_width)
            turtle.left(90)
            turtle.forward(2 * self.canvas_height)
            turtle.left(90)

    def __redraw(self):
        turtle.clear()
        self.my_number.clear()
        self.__draw_border()
        for i in range(0, 10):
            self.my_number.draw()
        for i in range(len(self.ball_list)):
            self.ball_list[i].draw()
        turtle.update()
        heapq.heappush(self.pq, my_event.Event(self.t + 1.0 / self.HZ, None, None))

    def run(self):
        # initialize pq with collision events and redraw event
        for i in range(len(self.ball_list)):
            self.__predict(self.ball_list[i])
        heapq.heappush(self.pq, my_event.Event(0, None, None))

        while (True):
            e = heapq.heappop(self.pq)
            if not e.is_valid():
                continue

            ball_a = e.a
            ball_b = e.b


            # update positions, and then simulation clock
            for i in range(len(self.ball_list)):
                self.ball_list[i].move(e.time - self.t)
            self.t = e.time

            if (ball_a is not None) and (ball_b is not None):
                ball_a.bounce_off(ball_b)
            elif (ball_a is not None) and (ball_b is None):
                ball_a.bounce_off_vertical_wall()
            elif (ball_a is None) and (ball_b is not None):
                ball_b.bounce_off_horizontal_wall()
            elif (ball_a is None) and (ball_b is None):
                self.__redraw()

            self.__predict(ball_a)
            self.__predict(ball_b)


        # hold the window; close it by clicking the window close 'x' mark
        turtle.done()




num_balls = 5
my_simulator = BouncingSimulator(num_balls)
my_simulator.run()
