from asammdf import MDF

def filter_mf4_by_channel_groups(input_path, output_path, keywords):
    """
    Filters an MF4 file, keeping only channels that contain specified keywords.
    
    Args:
        input_path (str): Path to input MF4 file
        output_path (str): Path to save filtered MF4 file
        keywords (list): List of keywords to match in channel group names
    """
    # Load the MF4 file
    with MDF(input_path) as mdf_file:
        # Get all channel groups
        channel_groups = mdf_file.groups
        print(channel_groups)
        
        # Find groups to keep (case-insensitive match)
        groups_to_keep = []
        for group_index, group in enumerate(channel_groups):
            # Check both the group name and channel names for keywords
            group_contains_keyword = any(
                any(keyword.lower() in str(name).lower() for keyword in keywords)
                for name in [group.channel_group.comment, *[ch.name for ch in group.channels]]
            )
            
            if group_contains_keyword:
                [groups_to_keep.append((ch.name, group_index)) for ch in group.channels]
        
        groups_to_keep = list(set(groups_to_keep))
        # Filter the MDF file
        filtered_mdf = mdf_file.filter(groups_to_keep)
        
        # Save the filtered file
        filtered_mdf.save(output_path, overwrite=True)


input_file = "C:\\Users\\carim\\Desktop\\Week of May 26 Trace files\\Concatenated MF4 decoded.mf4"
output_file = "C:\\Users\carim\\Desktop\\Week of May 26 Trace files\\filtered_output.mf4"
keywords = ["imd"] 

filter_mf4_by_channel_groups(input_file, output_file, keywords)