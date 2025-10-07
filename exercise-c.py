class Employee:
    def __init__(self, emp_id, name, role, hours_worked, hourly_rate, sales=0):
        required_fields = [emp_id, name, role, hours_worked, hourly_rate, sales]
        if any(v is None for v in required_fields):
            raise ValueError("All fields (emp_id, name, role, hours_worked, hourly_rate, sales) are required.")

        if hours_worked < 0 or hourly_rate < 0 or sales < 0:
            raise ValueError("hours_worked, hourly_rate, and sales cannot be negative.")

        self.emp_id = emp_id
        self.name = name
        self.role = role
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate
        self.sales = sales

    def gross_pay(self):
        base_pay = self.hours_worked * self.hourly_rate
        if self.hours_worked > 40:
            overtime_hours = self.hours_worked - 40 # 42 = 2 overtime hours
            overtime_multiplier = 1.5 * self.hourly_rate # 1.5 * 15 = 22.5
            overtime_pay = overtime_hours * overtime_multiplier # 2 * 22.5 = 45 (IN USD)
            total_gross_pay_with_overtime = base_pay + overtime_pay
            print(f"Payslip for {self.name}: \n"
                  f"Gross pay: {self.hours_worked}*{self.hourly_rate} = {base_pay} + overtime {overtime_hours}*{overtime_multiplier} = {overtime_pay} => {total_gross_pay_with_overtime}")
            return total_gross_pay_with_overtime
        else:
            total_gross_pay_without_overtime = base_pay
            print(f"Payslip for: {self.name}\n"
                  f"Gross pay: {self.hours_worked}*{self.hourly_rate} = {base_pay}")
            return total_gross_pay_without_overtime


class Department:
    def __init__(self, dept_id, department_name, employees):
        self.dept_id = dept_id
        self.department_name = department_name
        self.employees = employees

    def add_employee(self, emp):
        if emp.role == "sales":
            dept_sales.employees.append(emp)
        elif emp.role == "dev":
            dept_dev.employees.append(emp)
        elif emp.role == "support":
            dept_support.employees.append(emp)
        else:
            print(f"Employee role not found.")

    def dept_payroll(self):
        total_gross = 0
        for emp in self.employees:
            total_gross += emp.gross_pay()
        return total_gross

class Payroll:
    def process_departments(self, dept_list):
        for department in dept_list:
            net_pay_list = []
            tax_list = []
            bonus_list = []
            total_payroll_cost = 0
            number_of_part_time_employees = 0

            for employee in department.employees:
                base_pay = employee.hours_worked * employee.hourly_rate
                gross_pay = employee.gross_pay()

                if employee.role == "sales" and employee.sales >= 5000:
                    commission = employee.sales * 0.05
                    print(f"Commission: 5% of {employee.sales} = {int(commission)}")
                else:
                    commission = 0
                    print(f"Commission: {commission}")

                if gross_pay >= 1000 and employee.hours_worked >= 20:
                    bonus = 100
                    print(f"Bonus: {bonus}")
                else:
                    bonus = 0
                    number_of_part_time_employees += 1 # add 1 when worker has less than 20 hrs worked
                    print(f"Bonus: {bonus} (Did not meet the requirements: {gross_pay} gross >= 1000 gross & {employee.hours_worked} hours >= 20 hours)")

                gross_total_pay = base_pay + gross_pay + commission + bonus

                if gross_total_pay <= 1000:
                    tax_to_be_applied = 0.1
                elif gross_total_pay <= 3000:
                    tax_to_be_applied = 0.15
                else:
                    tax_to_be_applied = 0.2

                tax = gross_total_pay * tax_to_be_applied
                print(f"Tax: ({int(tax_to_be_applied * 100)}%): {int(tax)}")

                net_pay = gross_total_pay - tax
                print(f"Net pay: {net_pay}\n")
                net_pay_list.append(net_pay)
                tax_list.append(tax)
                bonus_list.append(bonus)
                total_payroll_cost = sum(net_pay_list) + sum(tax_list) + sum(bonus_list)

            department_name = department.department_name
            print(f"{department_name.upper()} DEPARTMENT SUMMARY")
            print(f"Total payroll cost (sum of net + taxes + bonuses): {total_payroll_cost}\n"
                  f"Number of part-time employees: {number_of_part_time_employees}\n"
                  f"Top earner (highest net): {max(net_pay_list)}\n"
                  f"--- --- --- --- --- --- --- --- --- ---\n")

dept_sales = Department(1, "Sales", [])
dept_dev = Department(2, "Dev", [])
dept_support = Department(3, "Support", [])

try:
    dept_sales.add_employee(Employee(1, "Ben", "sales", 38, 15, sales=6000))
    dept_sales.add_employee(Employee(2, "Neb", "sales", 19, 13))  # explicitly add sales
    dept_sales.add_employee(Employee(3, "Ana", "dev", 45, 20))
    dept_dev.add_employee(Employee(4, "Cara", "support", 15, 12))
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

payroll = Payroll()
departments = [dept_sales, dept_dev, dept_support]
payroll.process_departments(departments)

# Exercise C