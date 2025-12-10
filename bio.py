from manim import *
import numpy as np


class BiochemAlgoViz(Scene):
    def construct(self):
        # 1. 介绍场景
        self.intro_scene()

        # 2. 数据预处理 (Main - Sub)
        main_curve, sub_curve, final_curve, axes = self.data_process_scene()

        # 3. 算法可视化 - 终点法 (One Point End)
        self.endpoint_method_scene(axes, final_curve)

        # 4. 算法可视化 - 两点速率法 (Two Point Rate / Fix Time)
        self.fix_time_method_scene(axes, final_curve)

        # 5. 算法可视化 - 动力学法 (Rate A / Kinetic)
        self.kinetic_method_scene(axes, final_curve)

    def intro_scene(self):
        title = Text("Biochemical Analysis Algorithms", font_size=40, color=BLUE).to_edge(UP)
        subtitle = Text("Visualization of CHandleResultData.cpp", font_size=24, color=GRAY).next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(subtitle))
        self.title = title

    def create_axes_manual(self):
        """手动创建不依赖 LaTeX 的坐标轴"""
        axes = Axes(
            x_range=[0, 60, 10],
            y_range=[0, 2.5, 0.5],
            x_length=9, y_length=5,
            axis_config={
                "include_tip": True,
                "include_numbers": False  # 关键：禁用自动数字生成
            },
        ).shift(DOWN * 0.5)

        # 手动添加 X 轴数字
        x_nums = VGroup()
        for x in range(0, 70, 10):
            t = Text(str(x), font_size=16).next_to(axes.c2p(x, 0), DOWN)
            x_nums.add(t)

        # 手动添加 Y 轴数字
        y_nums = VGroup()
        for y in [0, 0.5, 1.0, 1.5, 2.0, 2.5]:
            t = Text(str(y), font_size=16).next_to(axes.c2p(0, y), LEFT)
            y_nums.add(t)

        # 手动添加标签
        x_label = Text("Test Points (Time)", font_size=20).next_to(axes.x_axis, RIGHT)
        y_label = Text("Absorbance", font_size=20).next_to(axes.y_axis, UP)

        return axes, x_nums, y_nums, x_label, y_label

    def data_process_scene(self):
        t_step1 = Text("Step 1: Dual Wavelength Correction", font_size=30, color=YELLOW).to_edge(UP).shift(DOWN * 1)
        self.play(Transform(self.title, t_step1))

        # 使用手动创建的坐标轴
        axes, x_nums, y_nums, x_label, y_label = self.create_axes_manual()
        self.play(Create(axes), Write(x_nums), Write(y_nums), Write(x_label), Write(y_label))

        # 模拟数据
        x_vals = np.linspace(0, 60, 100)
        # 主波长
        y_main = 0.5 + 1.5 * (1 - np.exp(-0.05 * x_vals)) + 0.05 * np.random.normal(0, 0.1, 100)
        # 副波长
        y_sub = 0.2 + 0.05 * np.sin(x_vals / 5)

        graph_main = axes.plot_line_graph(x_vals, y_main, add_vertex_dots=False, line_color=BLUE)
        graph_sub = axes.plot_line_graph(x_vals, y_sub, add_vertex_dots=False, line_color=RED)

        l_main = Text("Main Wave", color=BLUE, font_size=20).next_to(graph_main, UP).shift(RIGHT * 2)
        l_sub = Text("Sub Wave", color=RED, font_size=20).next_to(graph_sub, DOWN).shift(RIGHT * 2)

        self.play(Create(graph_main), Write(l_main))
        self.play(Create(graph_sub), Write(l_sub))
        self.wait(1)

        # 演示相减 (Text 替代 MathTex)
        formula = Text("Abs_final = Abs_main - Abs_sub", font_size=24).to_corner(UR)
        self.play(Write(formula))

        # 计算差值曲线
        y_final = y_main - y_sub
        graph_final = axes.plot_line_graph(x_vals, y_final, add_vertex_dots=False, line_color=GREEN)
        l_final = Text("Corrected Curve", color=GREEN, font_size=20).next_to(graph_final, UP)

        self.play(
            Transform(graph_main, graph_final),
            Transform(l_main, l_final),
            FadeOut(graph_sub), FadeOut(l_sub)
        )
        self.wait(1)

        return graph_main, None, y_final, axes

    def endpoint_method_scene(self, axes, y_data):
        t_info = Text("Method A: End Point (OnePointEnd)", font_size=30, color=GREEN).to_edge(UP).shift(DOWN * 1)
        self.play(Transform(self.title, t_info))

        # 假设 Start Point = 50
        x_idx_approx = 50
        # y_data是100个点对应0-60，所以索引大概是 50/60 * 100 = 83
        val_1 = y_data[83]
        val_2 = y_data[81]

        dot1 = Dot(axes.c2p(50, val_1), color=YELLOW)
        dot2 = Dot(axes.c2p(49, val_2), color=YELLOW)

        line_drop = DashedLine(dot1.get_center(), axes.c2p(50, 0), color=YELLOW)
        label_point = Text("Start Point", font_size=20).next_to(line_drop, DOWN)

        self.play(FadeIn(dot1), FadeIn(dot2), Create(line_drop), Write(label_point))

        # 公式 (Text)
        formula = Text("Result = (Abs(T) + Abs(T-1)) / 2", font_size=24).to_corner(UR)
        self.play(Write(formula))

        # 结果线
        avg_val = (val_1 + val_2) / 2
        res_line = Line(axes.c2p(0, avg_val), axes.c2p(50, avg_val), color=GREEN)
        self.play(Create(res_line))

        self.wait(2)
        self.play(FadeOut(dot1), FadeOut(dot2), FadeOut(line_drop), FadeOut(label_point), FadeOut(formula),
                  FadeOut(res_line))

    def fix_time_method_scene(self, axes, y_data):
        t_info = Text("Method B: Two Point Rate (Fix Time)", font_size=30, color=ORANGE).to_edge(UP).shift(DOWN * 1)
        self.play(Transform(self.title, t_info))

        start_time = 20
        end_time = 50
        y_start = y_data[int(start_time / 60 * 100)]
        y_end = y_data[int(end_time / 60 * 100)]

        dot_s = Dot(axes.c2p(start_time, y_start), color=ORANGE)
        dot_e = Dot(axes.c2p(end_time, y_end), color=ORANGE)

        l_s = Text("Start", font_size=16).next_to(dot_s, UP)
        l_e = Text("End", font_size=16).next_to(dot_e, UP)

        self.play(FadeIn(dot_s), FadeIn(dot_e), Write(l_s), Write(l_e))

        secant_line = Line(dot_s.get_center(), dot_e.get_center(), color=YELLOW, stroke_width=4)
        self.play(Create(secant_line))

        line_dx = Line(dot_s.get_center(), [dot_e.get_center()[0], dot_s.get_center()[1], 0], color=WHITE)
        line_dy = Line([dot_e.get_center()[0], dot_s.get_center()[1], 0], dot_e.get_center(), color=WHITE)

        # Text 替代 MathTex
        label_dx = Text("Delta T", font_size=20).next_to(line_dx, DOWN)
        label_dy = Text("Delta Abs", font_size=20).next_to(line_dy, RIGHT)

        self.play(Create(line_dx), Create(line_dy), Write(label_dx), Write(label_dy))

        formula = Text("Rate = (Delta Abs / Delta T) * 60", font_size=24).to_corner(UR)
        note = Text("*Includes Volume Correction", font_size=16, color=GRAY).next_to(formula, DOWN)

        self.play(Write(formula), FadeIn(note))
        self.wait(2)

        self.play(
            FadeOut(Group(dot_s, dot_e, l_s, l_e, secant_line, line_dx, line_dy, label_dx, label_dy, formula, note)))

    def kinetic_method_scene(self, axes, y_data):
        t_info = Text("Method C: Kinetic (Rate A)", font_size=30, color=RED).to_edge(UP).shift(DOWN * 1)
        self.play(Transform(self.title, t_info))

        start_idx = int(30 / 60 * 100)
        end_idx = int(50 / 60 * 100)

        dots = VGroup()
        x_seg = []
        y_seg = []

        for i in range(start_idx, end_idx, 2):
            x_val = i * 60 / 100
            y_val = y_data[i]
            x_seg.append(x_val)
            y_seg.append(y_val)
            dots.add(Dot(axes.c2p(x_val, y_val), color=RED, radius=0.05))

        self.play(Create(dots))

        slope, intercept = np.polyfit(x_seg, y_seg, 1)

        x1, x2 = 25, 55
        y1 = slope * x1 + intercept
        y2 = slope * x2 + intercept

        reg_line = Line(axes.c2p(x1, y1), axes.c2p(x2, y2), color=YELLOW, stroke_width=4)

        lbl_lsq = Text("Least Squares Fit", font_size=24, color=YELLOW).next_to(reg_line, UP).rotate(0.2)

        self.play(Create(reg_line), Write(lbl_lsq))

        formula = Text("Slope = Sum((T-avgT)(A-avgA)) / Sum(T-avgT)^2", font_size=18).to_corner(UR)

        self.play(Write(formula))
        self.wait(3)


if __name__ == "__main__":
    from manim import config

    config.background_color = BLACK
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
    config.output_file = "Biochem_Algo_Viz.mp4"
    config.preview = True

    scene = BiochemAlgoViz()
    scene.render()
