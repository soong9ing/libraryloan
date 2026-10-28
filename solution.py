# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14


def _valid_day(day):
    # bool은 int의 하위 클래스이므로 따로 제외한다.
    return isinstance(day, int) and not isinstance(day, bool) and day >= 1


class LibraryLoan:
    def __init__(self):
        self.loans = {}            # book_id -> (name, borrow_day, due_day)
        self.suspended_until = {}  # name -> 대출 정지 마지막 날 (포함)

    def borrow(self, book_id, name, day):
        if book_id not in BOOKS:
            return False
        if not _valid_day(day):
            return False
        if book_id in self.loans:
            return False
        held = [due for (who, _, due) in self.loans.values() if who == name]
        if len(held) >= 3:
            return False
        if any(day > due for due in held):
            return False
        if day <= self.suspended_until.get(name, 0):
            return False
        self.loans[book_id] = (name, day, day + LOAN_DAYS)
        return True

    def return_book(self, book_id, name, day):
        if not _valid_day(day):
            return -1
        loan = self.loans.get(book_id) if book_id in BOOKS else None
        if loan is None or loan[0] != name:
            return -1
        _, borrow_day, due = loan
        if day < borrow_day:
            return -1
        del self.loans[book_id]
        overdue = max(0, day - due)
        if overdue > 0:
            # 반납한 날부터 overdue일 동안 정지: day ~ day + overdue - 1
            end = day + overdue - 1
            self.suspended_until[name] = max(self.suspended_until.get(name, 0), end)
        return overdue

    def get_loans(self, name):
        result = [(b, due) for b, (who, _, due) in self.loans.items() if who == name]
        result.sort(key=lambda x: (x[1], x[0]))
        return result
