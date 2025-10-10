from env import PandaObstacleEnv
import mujoco
import mujoco.viewer

env = PandaObstacleEnv()
# 使用 env.reset() 初始化环境状态
obs, info = env.reset(seed=0)

# 设置循环参数，避免窗口立即关闭
max_episodes = 4
steps_per_episode = 500

# 用 mujoco.viewer.launch_passive 打开交互窗口（阻塞直到窗口关闭）
with mujoco.viewer.launch_passive(env.model, env.data) as viewer:
    for ep in range(max_episodes):
        # 每个 episode 内进行若干步
        for step in range(steps_per_episode):
            # 如果窗口被关闭，退出所有循环
            if not viewer.is_running():
                break

            action = env.action_space.sample()  # 示例：随机动作
            obs, reward, terminated, truncated, info = env.step(action)
            print(f"Step {step}, Reward: {reward:.3f}, Terminated: {terminated}, Truncated: {truncated}, action: {action}")

            # 同步 viewer 显示当前仿真状态
            viewer.sync()

            # 如果 episode 提前结束，则跳出当前 episode 循环
            if terminated or truncated:
                break

        # 如果窗口被关闭，结束外层循环
        if not viewer.is_running():
            break

        # episode 结束后重置环境以开始下一个 episode
        obs, info = env.reset()

env.close()




