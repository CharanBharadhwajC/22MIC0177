def solve_knapsack(tasks, capacity):
    n = len(tasks)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        duration = tasks[i - 1]["Duration"]
        impact = tasks[i - 1]["Impact"]
        for w in range(capacity + 1):
            if duration <= w:
                dp[i][w] = max(
                    impact + dp[i - 1][w - duration],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]
    w = capacity
    selected_tasks = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_tasks.append(tasks[i - 1])
            w -= tasks[i - 1]["Duration"]
    selected_tasks.reverse()
    return selected_tasks, dp[n][capacity]