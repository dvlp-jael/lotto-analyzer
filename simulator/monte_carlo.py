# simulator/monte_carlo.py
# 로또 몬테카를로 시뮬레이터 - 전략별 손익 비교

import numpy as np
import pandas as pd
import random

# 로또 당첨 기준 (매칭 개수 → 등수)
PRIZE_RULES = {
    6: {"등수": "1등", "금액": 2_000_000_000},  # 평균 20억 가정
    5.5: {"등수": "2등", "금액": 60_000_000},   # 보너스 포함 5개, 평균 6천만
    5: {"등수": "3등", "금액": 1_500_000},      # 평균 150만
    4: {"등수": "4등", "금액": 50_000},         # 고정 5만
    3: {"등수": "5등", "금액": 5_000},          # 고정 5천
}
TICKET_PRICE = 1_000  # 1장 가격

def generate_random_numbers():
    """완전 랜덤 번호 생성"""
    return sorted(random.sample(range(1, 46), 6))

def generate_hot_numbers(hot_list, size=6):
    """자주 나온 번호 위주로 생성"""
    pool = list(hot_list) + list(range(1, 46))
    seen = set()
    result = []
    for n in pool:
        if n not in seen:
            seen.add(n)
            result.append(n)
        if len(result) == 45:
            break
    return sorted(random.sample(result[:15], size))  # 상위 15개 중 6개

def generate_cold_numbers(cold_list, size=6):
    """안 나온 번호 위주로 생성"""
    pool = list(cold_list) + list(range(1, 46))
    seen = set()
    result = []
    for n in pool:
        if n not in seen:
            seen.add(n)
            result.append(n)
        if len(result) == 45:
            break
    return sorted(random.sample(result[:15], size))

def check_match(my_numbers, winning_numbers, bonus):
    """당첨 번호와 매칭 확인"""
    my_set = set(my_numbers)
    win_set = set(winning_numbers)
    matched = len(my_set & win_set)

    # 2등 체크 (5개 + 보너스)
    if matched == 5 and bonus in my_set:
        return 5.5
    return matched

def get_prize(match_count):
    """매칭 수에 따른 당첨금 반환"""
    return PRIZE_RULES.get(match_count, {}).get("금액", 0)

def simulate(strategy, weeks, df_history=None):
    """
    전략별 시뮬레이션
    strategy: 'random' | 'hot' | 'cold' | 'fixed'
    weeks: 시뮬레이션 회차 수
    """
    # 실제 당첨 번호 사용 (df_history 있으면)
    if df_history is not None:
        actual_rounds = df_history.tail(weeks)
        use_actual = len(actual_rounds) >= weeks
    else:
        use_actual = False

    # 핫/콜드 번호 준비
    if df_history is not None:
        number_cols = ["1번", "2번", "3번", "4번", "5번", "6번"]
        all_nums = df_history[number_cols].values.flatten()
        freq = pd.Series(all_nums).value_counts()
        hot_list = list(freq.nlargest(15).index)
        cold_list = list(freq.nsmallest(15).index)
    else:
        hot_list = list(range(30, 46))
        cold_list = list(range(1, 16))

    total_spent = 0
    total_won = 0
    prize_counts = {r: 0 for r in ["1등", "2등", "3등", "4등", "5등", "꽝"]}
    weekly_balance = []

    # 고정 번호 (fixed 전략용)
    fixed_numbers = generate_random_numbers()

    for i in range(weeks):
        # 내 번호 선택
        if strategy == "random":
            my_numbers = generate_random_numbers()
        elif strategy == "hot":
            my_numbers = generate_hot_numbers(hot_list)
        elif strategy == "cold":
            my_numbers = generate_cold_numbers(cold_list)
        elif strategy == "fixed":
            my_numbers = fixed_numbers
        else:
            my_numbers = generate_random_numbers()

        # 당첨 번호 결정
        if use_actual:
            row = actual_rounds.iloc[i]
            winning = [row["1번"], row["2번"], row["3번"],
                      row["4번"], row["5번"], row["6번"]]
            bonus = row["보너스"]
        else:
            winning = generate_random_numbers()
            bonus = random.choice([n for n in range(1, 46) if n not in winning])

        # 매칭 확인
        match = check_match(my_numbers, winning, bonus)
        prize = get_prize(match)

        total_spent += TICKET_PRICE
        total_won += prize

        # 등수 기록
        if match == 6:
            prize_counts["1등"] += 1
        elif match == 5.5:
            prize_counts["2등"] += 1
        elif match == 5:
            prize_counts["3등"] += 1
        elif match == 4:
            prize_counts["4등"] += 1
        elif match == 3:
            prize_counts["5등"] += 1
        else:
            prize_counts["꽝"] += 1

        weekly_balance.append(total_won - total_spent)

    return {
        "전략": strategy,
        "총투자": total_spent,
        "총당첨": total_won,
        "순손익": total_won - total_spent,
        "수익률": round((total_won - total_spent) / total_spent * 100, 2),
        "당첨현황": prize_counts,
        "누적손익": weekly_balance
    }

def run_all_strategies(weeks=100, df_history=None):
    """4가지 전략 모두 시뮬레이션"""
    strategies = ["random", "hot", "cold", "fixed"]
    results = []

    for s in strategies:
        result = simulate(s, weeks, df_history)
        results.append(result)
        print(f"[{s}] 투자: {result['총투자']:,}원 | "
              f"당첨: {result['총당첨']:,}원 | "
              f"손익: {result['순손익']:,}원 | "
              f"수익률: {result['수익률']}%")

    return results

if __name__ == "__main__":
    # 테스트
    import sys
    sys.path.append(".")
    from analyzer.stats import load_data

    print("=== 로또 몬테카를로 시뮬레이션 (100회차) ===\n")
    df = load_data()
    results = run_all_strategies(weeks=100, df_history=df)

    print("\n=== 당첨 현황 ===")
    for r in results:
        print(f"\n[{r['전략']}]")
        for grade, count in r["당첨현황"].items():
            print(f"  {grade}: {count}회")