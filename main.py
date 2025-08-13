from tkinter import Tk, Label, Button, Entry, Frame
from tkinter import ttk
from dataclasses import dataclass

months = {
    "January": 31,
    "February": 29,
    "March": 31,
    "April": 30,
    "May": 31,
    "June": 30,
    "July": 31,
    "August": 31,
    "September": 30,
    "October": 31,
    "November": 30,
    "December": 31,
}


@dataclass
class Time:
    hour: int
    min: int
    sec: int

    def __str__(self):
        return f"{self.hour}h {self.min}m and {self.sec}s"

    def ToPercent(self) -> float:
        total_seconds_in_day = 86400
        total_seconds = self.hour * 3600 + self.min * 60 + self.sec
        return total_seconds / total_seconds_in_day

    def ToDate(self) -> "Date":
        percent = self.ToPercent()
        print(f"Percent of the day: {percent}")

        if not (0.0 <= percent <= 1.0):
            raise ValueError("Percent must be between 0.0 and 1.0")

        total_days = percent * 365
        month = 1

        for i, days_in_month in enumerate(months.values()):
            if total_days > days_in_month:
                total_days -= days_in_month
                month += 1
            else:
                break

        day = int(total_days) + 1
        return Date(day, month)


@dataclass
class Date:
    day: int
    month: int

    def __str__(self):
        return f"{list(months.keys())[self.month-1]} {self.day}"

    def ToPercent(self) -> float:
        total_days = 365
        days = 0
        for m in months:
            if m == list(months.keys())[self.month - 1]:
                break
            days += months[m]
        days += self.day

        return (days - 1) / total_days

    def To24H(self) -> Time:
        percent = self.ToPercent()

        if not (0.0 <= percent <= 1.0):
            raise ValueError("Percent must be between 0.0 and 1.0, ", percent)

        total_minutes_in_day = 1440
        minutes_of_day = percent * total_minutes_in_day
        hours = int(minutes_of_day // 60)
        minutes = int(minutes_of_day % 60)
        seconds = int((minutes_of_day % 1) * 60)
        print(f"{hours:02}:{minutes:02}:{seconds:02}")

        return Time(hours, minutes, seconds)


if __name__ == "__main__":
    fenetre = Tk()
    fenetre.title("NewYear time Converter")

    label = Label(fenetre, text="HAPPY NEW YEAR", font=("Arial", 24))
    label.pack(pady=10)

    tabControl = ttk.Notebook(fenetre)

    tabToTime = ttk.Frame(tabControl)
    tabToDate = ttk.Frame(tabControl)

    tabControl.add(tabToTime, text="Convert Date to NewYear Time")
    tabControl.add(tabToDate, text="Convert NewYear Time to Date")

    tabControl.pack(expand=1, fill="both")

    ## Tab to convert Date to NewYear Time

    DatePanel = Frame(tabToTime, padx=20, pady=10)

    MonthLabel = Label(DatePanel, text="Month")
    MonthLabel.grid(column=0, row=0)

    MonthCombo = ttk.Combobox(DatePanel, values=list(months.keys()))
    MonthCombo.grid(column=0, row=1, padx=5)
    MonthCombo.current(0)  # Set default value to the first month

    DayLabel = Label(DatePanel, text="Day")
    DayLabel.grid(column=1, row=0)

    DayEntry = Entry(DatePanel)
    DayEntry.grid(column=1, row=1, padx=5)

    DatePanel.pack()

    ConvertedDate = Label(DatePanel)

    ConvertBtn = Button(
        DatePanel,
        text="Convert to NewYear Format",
        command=lambda: ConvertedDate.config(
            text="the NewYear Time is "
            + str(
                Date(
                    int(DayEntry.get()), int(list(months).index(MonthCombo.get()) + 1)
                ).To24H()
            )
        ),
    )
    ConvertBtn.grid(column=0, row=2, columnspan=3, pady=10)

    ConvertedDate.grid(column=0, row=3, columnspan=3, pady=5)

    ## Tab to convert NewYear Time to Date

    TimePanel = Frame(tabToDate, padx=20, pady=10)

    HourLabel = Label(TimePanel, text="Hour")
    HourLabel.grid(column=0, row=0)
    HourEntry = Entry(TimePanel)
    HourEntry.grid(column=0, row=1, padx=5)
    MinLabel = Label(TimePanel, text="Minute")
    MinLabel.grid(column=1, row=0)
    MinEntry = Entry(TimePanel)
    MinEntry.grid(column=1, row=1, padx=5)

    Convertedtime = Label(DatePanel)

    ConvertBtn2 = Button(
        TimePanel,
        text="Convert to Date",
        command=lambda: Convertedtime.config(
            text="the date is "
            + str(Time(int(HourEntry.get()), int(MinEntry.get()), 0).ToDate())
        ),
    )
    ConvertBtn2.grid(column=0, row=2, columnspan=3, pady=10)
    Convertedtime = Label(TimePanel)
    Convertedtime.grid(column=0, row=3, columnspan=3, pady=5)
    TimePanel.pack()

    fenetre.mainloop()
