from booking.booking import Booking
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(currency='INR')
        bot.select_places_to_go(input("Where you want to go?\n"))
        bot.select_dates(check_in_date=input('What is the check-in date?\n'),
                        check_out_date=input('What is the check-out date?\n'))
        bot.select_adults(int(input('How many people?\n')))
        bot.click_search()
        bot.apply_filterations()
        bot.refresh() # a work around to get the data properly
        bot.export_results()


except Exception as e:
    if 'in PATH' in str(e):
       print("There is a problem running this program from command line interface")
    else:
        raise