import gather_and_store
import process_and_visualize
    

def main():
    db_filename = 'sports.db'
        
    # Part 2
    gather_and_store.populate_baseball_table(db_filename)
    gather_and_store.populate_basketball_table(db_filename)
    gather_and_store.populate_football_table(db_filename)
    gather_and_store.populate_soccer_table(db_filename)
    
    # Part 3
    process_and_visualize.calculate_ratios(db_filename, 'baseball')
    process_and_visualize.calculate_ratios(db_filename, 'basketball')
    process_and_visualize.calculate_ratios(db_filename, 'football')
    process_and_visualize.calculate_ratios(db_filename, 'soccer')

    # Part 4
    process_and_visualize.visualize('baseball')
    process_and_visualize.visualize('basketball')
    process_and_visualize.visualize('football')
    process_and_visualize.visualize('soccer')

    # Extra visualization
    process_and_visualize.extra_visualization(db_filename)
    

if __name__ == "__main__":
    main()
    
    
