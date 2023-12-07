import gather_and_store
import process_and_visualize
    

def main():
    """
    Top level program function. 
    Executes Part 2 using gather_and_store, then Parts 3 and 4 using calculate_and_visualize. 
    Also creates an extra visualization. 

    Parameters
    -----------------------
    None

    Returns
    -----------------------
    None
    """

    sports = ['baseball', 'basketball', 'football', 'soccer']
        
    # Part 2 - Gather data, store to database
    gather_and_store.populate_baseball_tables()
    gather_and_store.populate_basketball_tables()
    gather_and_store.populate_football_tables()
    gather_and_store.populate_soccer_tables()

    # Part 3 - Calculate percentages, write to text files
    for sport in sports:
        process_and_visualize.calculate_ratios(sport)

    # Part 4 - Reads text files and creates visualizations
    for sport in sports:
        process_and_visualize.visualize(sport)

    # Extra visualization (with JOIN)
    process_and_visualize.extra_visualization()
    

if __name__ == "__main__":
    main()
    
    
