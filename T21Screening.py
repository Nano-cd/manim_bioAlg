from manim import *
import scipy.stats as stats
import numpy as np
import math


# 如果直接运行脚本，请保留文件末尾的 if __name__ == "__main__": 块

class T21ScreeningProcess(Scene):
    def construct(self):
        # === 全局配置与模拟数据 ===
        self.data = {
            "age": 38,
            "weight": 75.0,
            "val_afp": 30.0,
            "val_hcg": 65.0,
            "median_afp": 35.0,
            "median_hcg": 30.0
        }

        self.intro_scene()
        mom_afp, mom_hcg = self.calculation_scene()
        lr_total = self.gaussian_analysis_scene(mom_afp, mom_hcg)
        self.risk_assessment_scene(self.data["age"], lr_total)

    def intro_scene(self):
        title = Text("T21 Screening Algorithm", font_size=48).to_edge(UP)
        subtitle = Text("Visualization of process", font_size=24, color=GRAY).next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(subtitle))
        self.title = title

    def calculation_scene(self):
        # 简化版：不使用 LaTeX 公式，使用普通文本
        t_info = Text("Step 1: Calculate MoM (Multiples of Median)", font_size=30, color=BLUE).to_edge(UP).shift(
            DOWN * 1)
        self.play(Transform(self.title, t_info))

        raw_mom_hcg = self.data['val_hcg'] / self.data['median_hcg']

        # 使用 Text 而不是 MathTex
        txt_calc = Text(f"Raw hCG MoM = {self.data['val_hcg']} / {self.data['median_hcg']} = {raw_mom_hcg:.2f}",
                        font_size=24)
        txt_calc.move_to(UP * 0.5)

        self.play(Write(txt_calc))
        self.wait(1)

        # 权重校正
        exp_mom = 0.28 + (43.0 / self.data['weight'])
        factor = 1.0 / exp_mom
        corr_mom_hcg = raw_mom_hcg * factor
        corr_mom_afp = (self.data['val_afp'] / self.data['median_afp']) * factor

        txt_corr = Text(f"Weight Correction Factor: {factor:.2f}", font_size=24).next_to(txt_calc, DOWN)
        txt_final = Text(f"Corrected hCG MoM = {corr_mom_hcg:.2f}", font_size=30, color=YELLOW).next_to(txt_corr, DOWN)

        self.play(Write(txt_corr))
        self.play(Write(txt_final))
        self.wait(1)

        self.play(FadeOut(txt_calc), FadeOut(txt_corr), FadeOut(txt_final))
        return corr_mom_afp, corr_mom_hcg

    def gaussian_analysis_scene(self, mom_afp, mom_hcg):
        t_info = Text("Step 2: Gaussian Likelihood (LR)", font_size=30, color=YELLOW).to_edge(UP).shift(DOWN * 1)
        self.play(Transform(self.title, t_info))

        axes = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[0, 3, 1],
            x_length=9, y_length=4,
            axis_config={"include_tip": True, "font_size": 20}
        ).shift(DOWN * 0.5)

        # 绘制曲线
        norm_mean, norm_std = 0.0, 0.15
        t21_mean, t21_std = 0.3, 0.18
        curve_norm = axes.plot(lambda x: stats.norm.pdf(x, norm_mean, norm_std), color=BLUE)
        curve_t21 = axes.plot(lambda x: stats.norm.pdf(x, t21_mean, t21_std), color=RED)

        self.play(Create(axes), Create(curve_norm), Create(curve_t21))

        # 标注
        t_norm = Text("Normal", color=BLUE, font_size=20).next_to(axes.c2p(0, 2.7), UP)
        t_t21 = Text("T21", color=RED, font_size=20).next_to(axes.c2p(0.3, 2.2), UP)
        self.play(Write(t_norm), Write(t_t21))

        # 患者位置
        log_hcg = math.log10(mom_hcg)
        line = axes.get_vertical_line(axes.c2p(log_hcg, 3), color=YELLOW)
        self.play(Create(line))

        # 计算高度
        y_norm = stats.norm.pdf(log_hcg, norm_mean, norm_std)
        y_t21 = stats.norm.pdf(log_hcg, t21_mean, t21_std)
        lr = y_t21 / y_norm

        dot_norm = Dot(axes.c2p(log_hcg, y_norm), color=BLUE)
        dot_t21 = Dot(axes.c2p(log_hcg, y_t21), color=RED)
        self.play(FadeIn(dot_norm), FadeIn(dot_t21))

        # 显示 LR 结果
        txt_lr = Text(f"LR (Height Ratio) = {y_t21:.2f} / {y_norm:.2f} = {lr:.2f}", font_size=28).to_edge(UP).shift(
            DOWN * 2)
        bg = BackgroundRectangle(txt_lr, fill_color=BLACK, fill_opacity=0.8)
        self.play(FadeIn(bg), Write(txt_lr))
        self.wait(2)

        self.play(FadeOut(Group(axes, curve_norm, curve_t21, t_norm, t_t21, line, dot_norm, dot_t21, txt_lr, bg)))
        return lr * 0.8  # 假定总LR

    def risk_assessment_scene(self, age, total_lr):
        t_info = Text("Step 3: Final Risk", font_size=30, color=GREEN).to_edge(UP).shift(DOWN * 1)
        self.play(Transform(self.title, t_info))

        prior = 150
        final_denom = prior / total_lr

        t1 = Text(f"Prior Risk (Age {age}): 1/{prior}", font_size=30).shift(UP)
        t2 = Text(f"Likelihood Ratio: {total_lr:.2f}", font_size=30)
        t3 = Text(f"Final Risk = 1 / ({prior} / {total_lr:.2f})", font_size=30).next_to(t2, DOWN)
        t4 = Text(f"Result: 1 : {int(final_denom)}", font_size=40, color=RED).next_to(t3, DOWN * 2)

        self.play(Write(t1), Write(t2))
        self.play(Write(t3))
        self.play(Write(t4))
        self.wait(2)


# === 这里就是让你能直接运行的关键 ===
if __name__ == "__main__":
    if __name__ == "__main__":
        from manim import config

        # === 1. 设置高清画质 ===
        config.background_color = BLACK
        config.pixel_height = 1080  # 1080p 高清
        config.pixel_width = 1920
        config.frame_rate = 60  # 60帧流畅动画

        # === 2. 设置保存文件名 ===
        # 视频将保存在 media/videos/mni/1080p60/ 文件夹下
        config.output_file = "T21筛查演示视频.mp4"

        config.preview = True  # 渲染完自动播放

        scene = T21ScreeningProcess()
        scene.render()
