import gather_and_store
import process_and_visualize
    

def main():
    sports = ['baseball', 'basketball', 'football', 'soccer']
        
    # Part 2
    for i in range(50):
        gather_and_store.populate_baseball_table()
        gather_and_store.populate_basketball_table()
        gather_and_store.populate_football_table()
        gather_and_store.populate_soccer_table()
    
    # Part 3
    for sport in sports:
        process_and_visualize.calculate_ratios(sport)

    # Part 4
    for sport in sports:
        process_and_visualize.visualize(sport)

    # Extra visualization
    process_and_visualize.extra_visualization()
    

if __name__ == "__main__":
    main()
    
    
