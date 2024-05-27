from collections import defaultdict


class ATM:
    # хранение в виде {номинал: количество}, например {10: 2, 50: 0, 100: 1}
    available_banknotes: dict[int, int]

    # ограничения
    denomination_cnt: int  # допустимое кол-во номиналов (видов банкнот)
    min_banknote_cnt: int  # мин. кол-во банкнот кажд. вида при внесении денег
    max_banknote_cnt: int  # макс. кол-во банкнот кажд. вида при внесении денег
    min_amount: int  # мин. сумма к выводу
    max_amount: int  # макс. сумма к выводу

    # вспомогательные справочники для перевода данных
    # из списка в словарь (и наоборот)
    index_to_banknote: dict[int, int]  # например {0: 10, 1: 50, 2: 100}
    banknote_to_index: dict[int, int]  # например {10: 0, 50: 1, 100: 2}

    def __init__(self, limitations: dict[str, int],
                 index_to_banknote: dict[int, int]):
        self.available_banknotes = defaultdict(lambda: 0)

        # ограничения
        self.denomination_cnt = limitations['denomination_count']
        self.min_banknote_cnt = limitations['min_banknote_count']
        self.max_banknote_cnt = limitations['max_banknote_count']
        self.min_amount = limitations['min_amount']
        self.max_amount = limitations['max_amount']

        # вспомогательные справочники
        self.index_to_banknote = index_to_banknote
        self.banknote_to_index = {v: k for k, v in index_to_banknote.items()}

    def deposit(self, banknotes_count: list[int]):
        if self.deposit_validation(banknotes_count):
            for index, banknote_cnt in enumerate(banknotes_count, 0):
                banknote_value = self.index_to_banknote[index]
                self.available_banknotes[banknote_value] += banknote_cnt

    def withdraw(self, amount: int) -> list[int]:
        if self.min_amount <= amount <= self.max_amount:
            banknotes_cnt = [0 for _ in range(self.denomination_cnt)]
            new_available_banknotes = self.available_banknotes.copy()
            for banknote in sorted(self.available_banknotes.keys(), reverse=True):
                if banknote <= amount and self.available_banknotes[banknote]:
                    amount -= banknote
                    new_available_banknotes[banknote] -= 1
                    banknotes_cnt[self.banknote_to_index[banknote]] += 1
            if amount == 0:
                self.available_banknotes.update(new_available_banknotes)
                return banknotes_cnt
        return [-1]

    def deposit_validation(self, banknotes_count: list[int]) -> bool:
        if len(banknotes_count) != self.denomination_cnt:
            return False
        for banknote_cnt in banknotes_count:
            if not (self.min_banknote_cnt <= banknote_cnt <=
                    self.max_banknote_cnt):
                return False
        return True


if __name__ == '__main__':
    atm_limitations = {
        'denomination_count': 5,
        'min_banknote_count': 0,
        'max_banknote_count': 10e9,
        'min_amount': 1,
        'max_amount': 10e9
    }

    index_to_banknote_schema = {
        0: 10,
        1: 50,
        2: 100,
        3: 200,
        4: 500
    }

    atm_obj = ATM(atm_limitations, index_to_banknote_schema)
    atm_obj.deposit([0, 0, 1, 2, 1])
    print(atm_obj.withdraw(600))  # [0, 0, 1, 0, 1]
    atm_obj.deposit([0, 1, 0, 1, 1])
    print(atm_obj.withdraw(600))  # [-1]
    print(atm_obj.withdraw(550))  # [0, 1, 0, 0, 1]

