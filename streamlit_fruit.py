"""
Demo of interactive filtering with Streamlit using dummy data
"""

import streamlit as st
import pandas as pd

# Dummy data
df = pd.DataFrame({
    'fruit': ['apple', 'banana', 'lemon', 'strawberry', 'cherry', 'raspberry'],
    'colour': ['green', 'yellow', 'yellow', 'red', 'red', 'red'],
    'hardness': ['hard', 'soft', 'hard', 'soft', 'soft', 'soft'],
    'weight': [250., 300., 200., 40., 20., 15.],
    'expiry': [pd.to_datetime(d) for d in ['2023-03-31','2023-03-10','2023-03-02','2023-03-01','2023-03-21','2023-03-11']],
    'description': [f'This is a {adj} fruit' for adj in ['round', 'bendy', 'citrus', 'delicious', 'stone', 'lovely',]],
    'origin': ['ontario', 'dominican republic', 'florida', 'ontario', 'bc', 'bc'],
    'shipper': ['clive', 'derek', 'james', 'ed', 'greg', 'alex'],
    'shipped': [pd.to_datetime(d) for d in ['2023-02-28','2023-02-10','2023-02-02','2023-02-01','2023-02-21','2023-02-11']],
})


def run():

    # Search query box plus filters to apply before searching
    st.title('Interactive Filter Test With Fruit')
    s = st.text_input('Type at least one character to search the fruit database').strip()
    colours_all = sorted(df['colour'].unique())
    hardness_all = sorted(df['hardness'].unique())
    c1, c2 = st.columns(2)
    colours_searched = c1.multiselect('Colours to search', colours_all, default=colours_all)
    hardness_searched = c2.multiselect('Hardness to search', hardness_all, default=hardness_all)

    def filter_df(s, c, h): # search, colours, hardness
        return df[df['fruit'].str.contains(s) & df['colour'].isin(c) & df['hardness'].isin(h)]

    # simulate search by retrieving filtered results
    df_after_search = filter_df(s, colours_searched, hardness_searched)

    searched = len(s) > 0
    if searched:
        text, expand = f'Full Results Searching For "{s}"', True
    else:
        text, expand = 'Enter a character in the search field above', False

    # show search results
    with st.expander(text, expanded=expand):
        if searched:
            st.dataframe(df_after_search, use_container_width=True)
        else:
            st.write('Nothing to see here until you serch for text.')

    # now set up refinement filters for different parameters, to allow refinement of the search results
    colours_for_refinement = list(sorted(df_after_search['colour'].unique()))
    hardness_for_refinement = list(sorted(df_after_search['hardness'].unique()))
    if searched and len(colours_for_refinement) > 0:
        with st.expander('**Refine Results**'):
            refine_1, refine_2 = st.columns(2)
            colours_after_refinement = refine_1.multiselect('Colour', colours_for_refinement, default=colours_for_refinement)
            hardness_after_refinement = refine_2.multiselect('Hardness', hardness_for_refinement, default=hardness_for_refinement)
            df_after_refinement = filter_df(s, colours_after_refinement, hardness_after_refinement)
            st.dataframe(df_after_refinement, use_container_width=True)
    else:
        colours_after_refinement = []
        df_after_refinement = pd.DataFrame()

    # Display a details section for a given set of display columns.  Must have a date col
    def display_details(details_title, date_col, display_columns):
        expander = st.expander(f'**{details_title}**', expanded=False)
        with expander:
            if len(df_after_refinement) > 0:  # have some results
                col1, col2 = st.columns(2)
                sort_by_date = col1.checkbox(f'Sort by {date_col} date')
                refine_dates = col2.checkbox(f'Refine by {date_col} date')
                min_date, max_date = df_after_refinement[date_col].min(), df_after_refinement[date_col].max()
                if refine_dates:
                    min_date_filter = pd.to_datetime(col1.date_input('Start Date', min_date, min_value=min_date, max_value=max_date))
                    max_date_filter = pd.to_datetime(col2.date_input('End Date', max_date, min_value=min_date, max_value=max_date))
                else:
                    min_date_filter = min_date
                    max_date_filter = max_date
                dfd = df_after_refinement  # convenience only; could filter in place below
                df_display = dfd[(dfd[date_col] >= min_date_filter) & (dfd[date_col] <= max_date_filter)]

                if sort_by_date:
                    df_display = df_display.sort_values(date_col)

                st.dataframe(df_display.loc[:, display_columns])
            else:
                st.write('Nothing to show here.  Try a different search and/or remove some filters.')

    display_details(details_title = 'Descriptions', date_col = 'expiry', display_columns = ['fruit', 'expiry', 'description'])
    display_details(details_title = 'Logistics', date_col = 'shipped', display_columns = ['fruit', 'shipped', 'origin', 'shipper', 'weight'])

if __name__ == '__main__':
    run()
