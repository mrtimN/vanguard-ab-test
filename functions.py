def check_error(df, possible_previous_steps):
    df = df.copy()
    df['error'] = False
    error_counts = {'Control': 0, 'Test': 0}
    visit_counts = {'Control': 0, 'Test': 0}
    
    for (visit_id, variation), group in df.groupby(['visit_id', 'Variation']):
        previous_step = None
        visit_counts[variation] += 1
        # iterate over the rows in the group
        for idx, row in group.iterrows():
            step = row['process_step']
                
            if previous_step is not None:
                # valid steps sequence (same step)
                if previous_step == step:
                    valid_count += 1
                    df.at[idx, 'error'] = False
                else:
                    expected_previous = possible_previous_steps.get(step)
                    # invalid step sequence (some step before current)
                    if previous_step != expected_previous:
                        error_counts[variation] += 1
                        df.at[idx, 'error'] = True
                    else:
                        # valid step sequence (next step)
                        df.at[idx, 'error'] = False
            # setting the current step as previous step for the next iteration
            previous_step = step
    return df