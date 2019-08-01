COLOR_CODES = {
    'green': '\033[92m',
    'red': '\033[91m',
    'end': '\033[0m',
}

def color_text(color, msg):
    code = COLOR_CODES[color]
    end = COLOR_CODES['end']

    return '%s%s%s' % (code, msg, end)


def prompt_for_float(prompt):
    hopefully_a_float = raw_input(prompt)

    try:
        a_float = float(hopefully_a_float)
    except:
        print(color_text('red', '\nPlease enter a number (digits and decimal-point only).'))
        return prompt_for_float(prompt)

    return a_float


def get_prev_balance():
    prompt = color_text('green', 'What was the balance in the venmo account before the first donation for this event (hopefully $0 >_>)?')
    prompt += '\n> $'
    return prompt_for_float(prompt)


def get_spent_amount():
    prompt = color_text('green', 'Enter the total amount spent on the camp this year (found in master spreadsheets "Expense tracking" tab).')
    prompt += '\n> $'
    return prompt_for_float(prompt)


def get_donation():
    prompt = 'Enter the donation amount: $'
    return prompt_for_float(prompt)


def get_name_donor_data():
    print(color_text('green', '\nEnter donor names and amounts of donations. Some amount may be refunded to donors, if there were excess donations.'))
    donor_data = []

    while True:
        more = raw_input('\nAdd another donation (y/n)?: ')

        if more is 'n':
            break
        elif more is not 'y':
            print(color_text('red', '\nPlease enter y or n.'))
            continue

        donor_name = raw_input('Enter the next donor name: ')

        if not donor_name:
            break
        
        donation_amount = get_donation()

        donor_data.append({
            'name': donor_name,
            'amount': donation_amount,
        })
    
    return donor_data


def calc_max_donation(prev_balance, donor_data, total_amount_spent):
    sorted_donor_data = sorted(
        donor_data,
        key = lambda i: i['amount'],
    )

    num_donors = len(sorted_donor_data)
    total_so_far = prev_balance

    for i in range(num_donors):
        people_remaining = num_donors - i
        current_amount = sorted_donor_data[i]['amount']

        theoretical_total = total_so_far + (people_remaining * current_amount)

        if theoretical_total >= total_amount_spent:
            spent_amt_remaining = total_amount_spent - total_so_far
            maximum_donation = spent_amt_remaining / people_remaining
            return maximum_donation
        else:
            total_so_far += sorted_donor_data[i]['amount']

    return -1


def print_output_headers():
    print('\n\n')
    print('| %-15s | %-8s | %-s' % ('', '', 'Amount Paid'))
    print('| %-15s | %-8s | %-s' % ('Name', 'Refund', 'After Refund'))
    print('-------------------------------------------')


def print_refund_row(name, refund_given, amt_after_refund):
    print('| %-15s | $%-7.2f | $%-.2f' % (name, refund_given, amt_after_refund))


def print_total_row(refund_given):
    print('-------------------------------------------')
    print('| %-15s | $%-7.2f |' % ('Total refunds', refund_given))


def calc_refund_quantities(donor_data, maximum_donation):
    num_donors = len(donor_data)
    total_refund = 0

    for i in range(num_donors):
        data = donor_data[i]
        name = data['name']
        amount = data['amount']
        amt_after_refund = amount
        refund_given = 0
        
        if amount > maximum_donation:
            amt_after_refund = maximum_donation
            refund_given = amount - maximum_donation

        donor_data[i]['refund'] = refund_given
        print_refund_row(name, refund_given, amt_after_refund)
        total_refund += refund_given

    print_total_row(total_refund)


def print_summary(donor_data, prev_balance, total_amount_spent, maximum_donation):
    num_donors = len(donor_data)
    total_donations = sum(
        map(
            lambda i: i['amount'],
            donor_data,
        ),
    )
    total_post_refund_donations = sum(
        map(
            lambda i: i['amount'] - i['refund'],
            donor_data,
        ),
    )

    avg_donation = total_donations / num_donors
    avg_pr_donation = total_post_refund_donations / num_donors

    total_refund_amount = sum(
        map(
            lambda i: i['refund'],
            donor_data,
        ),
    )

    print('\n\n')
    print('Summary')
    print('-------')
    print('Number of donors: %i' % num_donors)
    print('Total donations: $%.2f' % total_donations)
    print('Average donation (mean): $%.2f' % avg_donation)
    print('Average donation after refund (mean): $%.2f' % avg_pr_donation)
    print('Maximum allowed donation: $%.2f' % maximum_donation)
    print('\n')
    print('Starting balance: $%.2f' % prev_balance)
    print('Amount spent this event: $%.2f' % total_amount_spent)
    print('Total refunded: $%.2f' % total_refund_amount)
    print('New balance (should be $0): $%.2f' % ((prev_balance + total_donations) - (total_amount_spent + total_refund_amount)))
    print('\n')


def calc_refunds():
    prev_balance = get_prev_balance()
    total_amount_spent = get_spent_amount()
    donor_data = get_name_donor_data()
    maximum_donation = calc_max_donation(prev_balance, donor_data, total_amount_spent)

    if maximum_donation < 0:
        print(color_text('red', '\nCosts exceeded donations. No refunds given.'))
        return

    print_output_headers()
    calc_refund_quantities(donor_data, maximum_donation)
    print_summary(donor_data, prev_balance, total_amount_spent, maximum_donation)


calc_refunds()
