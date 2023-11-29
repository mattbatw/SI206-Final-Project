# project files
import gather_and_store
import analyze_and_visualize

def main():
  db_filename = 'sports.db'
     
  gather_and_store.populate_baseball_table(db_filename, table_name='baseball')
  gather_and_store.populate_basketball_table(db_filename, table_name='basketball')
  # gather_and_store.populate_soccer_table(db_filename, table_name='soccer')
  # gather_and_store.populate_hockey_table(db_filename, table_name='hockey')

  # txt files being weird

  # also check away teams when getting team list in analyze and visualize

  analyze_and_visualize.calculate_ratios(db_filename, table_name='baseball', txt_filename='baseball.txt')
  analyze_and_visualize.calculate_ratios(db_filename, table_name='basketball', txt_filename='basketball.txt')
  # analyze_and_visualize.calculate_ratios(db_filename, table_name='hockey', txt_filename='hockey.txt')
  # analyze_and_visualize.calculate_ratios(db_filename, table_name='soccer', txt_filename='soccer.txt')

if __name__ == "__main__":
  main()
