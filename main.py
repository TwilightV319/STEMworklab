from janim.imports import *


class EulerAngleRotation(Timeline):
    CONFIG = Config(
        font='Microsoft YaHei',
    )

    def construct(self):  
        # 旋转相机到接近对角线 (1,1,1) 的方向，以便同时看到三个完整的坐标轴
        self.camera.points.set(orientation=quat(-0.25, 0.14, 0.04, 0.96))
        self.camera.points.scale(0.9)  # 略微拉近镜头，使坐标轴更突出

        # 旋转参数（欧拉角 Z-X'-Z''）
        phi = PI / 4      # 第一次绕 z 轴旋转
        theta = PI / 3    # 第二次绕 x' 轴旋转
        psi = PI / 6      # 第三次绕 z'' 轴旋转

        axis_len = 1.8
        lbl_offset = axis_len + 0.35

        # 原始坐标系（白色），不旋转坐标系本身
        # z轴 UP，y轴 RIGHT，x轴 OUT
        ox = Arrow(ORIGIN, OUT * axis_len, color=WHITE, buff=0)
        oy = Arrow(ORIGIN, RIGHT * axis_len, color=WHITE, buff=0)
        oz = Arrow(ORIGIN, UP * axis_len, color=WHITE, buff=0)

        ox_lbl = Text('x', font_size=26, color=WHITE)
        ox_lbl.points.next_to(ox, OUT, buff=0.15)
        oy_lbl = Text('y', font_size=26, color=WHITE)
        oy_lbl.points.next_to(oy, RIGHT, buff=0.15)
        oz_lbl = Text('z', font_size=26, color=WHITE)
        oz_lbl.points.next_to(oz, UP, buff=0.15)

        orig_arrows = Group(ox, oy, oz)
        orig_labels = Group(ox_lbl, oy_lbl, oz_lbl)

        # 标题（固定在画面上，正对屏幕）
        title = Text("欧拉角 ", font_size=30, color=YELLOW)
        title.points.move_to(UP * 3.2)
        title.fix_in_frame().show()

        # 时间轴严格分离：标题先写出，再创建原始坐标系
        self.play(Write(title))
        self.forward(0.3)
        self.play(Create(orig_arrows), Create(orig_labels))
        self.forward()

        # 原地复制坐标轴箭头（与原始坐标系完全重合于原点）
        rot_arrows = orig_arrows.copy()

        # 改变颜色以区分（旋转坐标系使用更鲜艳的颜色）
        rot_arrows[0].color.set(RED)     # x 轴
        rot_arrows[1].color.set(GREEN)   # y 轴
        rot_arrows[2].color.set(BLUE)    # z 轴

        # 旋转坐标轴的标签：作为子物件加入箭头组，随坐标轴一起旋转
        rx_lbl = Text('x', font_size=26, color=RED)
        ry_lbl = Text('y', font_size=26, color=GREEN)
        rz_lbl = Text('z', font_size=26, color=BLUE)

        # 标签初始位置
        rx_lbl.points.move_to(OUT * lbl_offset)
        ry_lbl.points.move_to(RIGHT * lbl_offset)
        rz_lbl.points.move_to(UP * lbl_offset)

        rot_arrows.add(rx_lbl, ry_lbl, rz_lbl)

        # 瞬时显示旋转坐标系，避免遮挡原始坐标系
        rot_arrows.show()

        # 创建与旋转之间仅停顿 0.3 秒
        self.forward(0.3)

        # 当前旋转坐标轴的方向（动态更新）
        x_dir = np.array(OUT, dtype=float)
        y_dir = np.array(RIGHT, dtype=float)
        z_dir = np.array(UP, dtype=float)

        # 步骤 1：绕 z 轴(UP)顺时针旋转 Φ（步骤文字固定在画面上，正对屏幕）
        step1 = Text('1. 绕 z 轴逆时针旋转 Φ', font_size=22, color=YELLOW)
        step1.points.move_to(DOWN * 3.0)
        step1.fix_in_frame().show()
        self.play(Write(step1))

        self.play(Rotate(rot_arrows, phi, axis=UP, about_point=ORIGIN, duration=2))

        # 标注 x 轴与 x' 轴之间的夹角 Φ
        arc_phi = ParametricCurve(
            lambda t: 0.5 * rotate_vector(OUT, t, UP),
            t_range=(0, phi, 0.05),
            color=WHITE,
        )
        lbl_phi = Text('Φ', font_size=22, color=WHITE)
        lbl_phi.points.move_to(0.8 * rotate_vector(OUT, phi / 2, UP))
        self.play(Create(arc_phi), Write(lbl_phi))

        # 更新最终方向
        x_dir = rotate_vector(x_dir, phi, axis=UP)
        y_dir = rotate_vector(y_dir, phi, axis=UP)
        z_dir = rotate_vector(z_dir, phi, axis=UP)

        self.forward(0.5)
        self.play(FadeOut(step1), FadeOut(arc_phi), FadeOut(lbl_phi))

        # 计算旋转后的 x' 方向
        x_prime = x_dir.copy()

        # 步骤 2：绕 x' 轴顺时针旋转 θ（步骤文字固定在画面上，正对屏幕）
        step2 = Text("2. 绕 x' 轴逆时针旋转 θ", font_size=22, color=YELLOW)
        step2.points.move_to(DOWN * 3.0)
        step2.fix_in_frame().show()
        self.play(Write(step2))

        self.play(Rotate(rot_arrows, theta, axis=x_prime, about_point=ORIGIN, duration=2))

        # 标注 z 轴与 z' 轴之间的夹角 θ
        arc_theta = ParametricCurve(
            lambda t: 0.5 * rotate_vector(UP, t, x_prime),
            t_range=(0, theta, 0.05),
            color=WHITE,
        )
        lbl_theta = Text('θ', font_size=22, color=WHITE)
        lbl_theta.points.move_to(0.8 * rotate_vector(UP, theta / 2, x_prime))
        self.play(Create(arc_theta), Write(lbl_theta))

        # 更新最终方向
        x_dir = rotate_vector(x_dir, theta, axis=x_prime)
        y_dir = rotate_vector(y_dir, theta, axis=x_prime)
        z_dir = rotate_vector(z_dir, theta, axis=x_prime)

        # 保存第二步结束后的 y' 方向，供后续显示虚线使用
        y_prime = y_dir.copy()

        self.forward(0.5)
        self.play(FadeOut(step2), FadeOut(arc_theta), FadeOut(lbl_theta))

        # 计算旋转两次后的 z'' 方向
        z_double_prime = z_dir.copy()

        # 步骤 3：绕 z'' 轴顺时针旋转 ψ（步骤文字固定在画面上，正对屏幕）
        step3 = Text("3. 绕 z'' 轴逆时针旋转 ψ", font_size=22, color=YELLOW)
        step3.points.move_to(DOWN * 3.0)
        step3.fix_in_frame().show()
        self.play(Write(step3))

        self.play(Rotate(rot_arrows, psi, axis=z_double_prime, about_point=ORIGIN, duration=2))

        # 更新最终方向
        x_dir = rotate_vector(x_dir, psi, axis=z_double_prime)
        y_dir = rotate_vector(y_dir, psi, axis=z_double_prime)

        # 第三步旋转结束后：显示第二步结束后的 x' 和 y' 虚线，并标记 x, y
        dashed_x = DashedLine(ORIGIN, x_prime * axis_len, color=WHITE)
        dashed_y = DashedLine(ORIGIN, y_prime * axis_len, color=WHITE)
        dashed_x_lbl = Text('x', font_size=26, color=WHITE)
        dashed_y_lbl = Text('y', font_size=26, color=WHITE)
        dashed_x_lbl.points.move_to(x_prime * lbl_offset)
        dashed_y_lbl.points.move_to(y_prime * lbl_offset)

        # 标注 ψ：第二步结束后的 x'（x_prime）与第三步结束后的 x'（x_dir）之间的夹角
        arc_psi = ParametricCurve(
            lambda t: 0.5 * rotate_vector(x_prime, t, z_double_prime),
            t_range=(0, psi, 0.05),
            color=WHITE,
        )
        lbl_psi = Text('ψ', font_size=22, color=WHITE)
        lbl_psi.points.move_to(0.8 * rotate_vector(x_prime, psi / 2, z_double_prime))

        self.play(
            Create(dashed_x), Create(dashed_y),
            Write(dashed_x_lbl), Write(dashed_y_lbl),
            Create(arc_psi), Write(lbl_psi),
        )

        self.forward(1)

        # 重新显示出前两步的两个角度（ψ 不消失）
        arc_phi = ParametricCurve(
            lambda t: 0.5 * rotate_vector(OUT, t, UP),
            t_range=(0, phi, 0.05),
            color=WHITE,
        )
        lbl_phi = Text('Φ', font_size=22, color=WHITE)
        lbl_phi.points.move_to(0.8 * rotate_vector(OUT, phi / 2, UP))

        arc_theta = ParametricCurve(
            lambda t: 0.5 * rotate_vector(UP, t, x_prime),
            t_range=(0, theta, 0.05),
            color=WHITE,
        )
        lbl_theta = Text('θ', font_size=22, color=WHITE)
        lbl_theta.points.move_to(0.8 * rotate_vector(UP, theta / 2, x_prime))

        self.play(
            Create(arc_phi), Write(lbl_phi),
            Create(arc_theta), Write(lbl_theta),
            FadeOut(step3),
        )

        self.forward(2)
