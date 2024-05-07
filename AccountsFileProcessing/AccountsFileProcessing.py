import csv
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(0)

def generate_fake_data(num_accounts):
    data = []
    for i in range(num_accounts):
        plan = fake.random_element(elements=('free', 'basic', 'full'))
        username = fake.user_name()
        last_login_date = fake.date_between(start_date='-1y', end_date='today')
        if plan != 'free':
            expire_date = fake.date_between(start_date=last_login_date, end_date='+1y')
        else:
            expire_date = None
        data.append([i + 1000, plan, username, last_login_date, expire_date])
    return data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["id", "plan", "username", "last_login_date", "expire_date"])
        csvwriter.writerows(data)

def load_from_csv(filename):
    data = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) 
        for row in csvreader:
            data.append([int(row[0]), row[1], row[2], row[3], row[4] if row[4] else None])
    return data

def print_total_accounts_per_plan(data):
    plan_counts = {'free': 0, 'basic': 0, 'full': 0}
    for row in data:
        plan_counts[row[1]] += 1
    for plan, count in plan_counts.items():
        print(f"Total {plan.capitalize()} Accounts: {count}")

def find_free_accounts_with_more_than_3_months(data):
    today = datetime.now().date()
    for row in data:
        if row[1] == 'free' and row[4]:
            expire_date = datetime.strptime(row[4], '%Y-%m-%d').date()
            if (expire_date - today) > timedelta(days=90):
                print(f"Free Account: {row[2]}, Expires on: {row[4]}")

def find_expired_basic_and_full_accounts(data):
    today = datetime.now().date()
    for row in data:
        if row[1] in ('basic', 'full') and row[4]:
            expire_date = datetime.strptime(row[4], '%Y-%m-%d').date()
            if expire_date < today:
                print(f"Expired {row[1].capitalize()} Account: {row[2]}, Expired on: {row[4]}")

if __name__ == "__main__":
    fake_data = generate_fake_data(1000)
    save_to_csv(fake_data, 'accounts.csv')

    loaded_data = load_from_csv('accounts.csv')

    while True:
        print("\nMenu:")
        print("1. Print Total Accounts per Plan")
        print("2. Find Free Accounts with More Than 3 Months to Login")
        print("3. Find Expired Basic and Full Accounts")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            print_total_accounts_per_plan(loaded_data)
        elif choice == "2":
            find_free_accounts_with_more_than_3_months(loaded_data)
        elif choice == "3":
            find_expired_basic_and_full_accounts(loaded_data)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please select a valid option.")
