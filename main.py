import streamlit as st
with st.echo(code_location='below'):
    #import streamlit as st
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    import altair as alt
    import plotly.express as px

    color = st.color_picker('Pick A Color what you want for relax', '#0FEEF3')
    @st.cache
    def get_data():
        data_url = ('gender_wage_gap.csv')
        return (pd.read_csv(data_url))
    df = get_data()
    df_TOT = df[df["SUBJECT"] == "TOT"]
    df_SELFEMPLOYED = df[df["SUBJECT"] == "SELFEMPLOYED"]
    def print_info(name="Dear"):
        st.write(f"### Hello, {name}! Here is the visualization of the gap in median "
                 f"earnings between men&women and men only. ")
        st.write("This data for full-time employees (TOT) and self-employed for both "
                 "men and women.")

    countries15_TOT = df_TOT["LOCATION"].unique().tolist()[0:14]
    data_of_15_countries_TOT = df_TOT[df_TOT["LOCATION"].isin(countries15_TOT)]
    countries15_SELFEMPLOYED = df_SELFEMPLOYED["LOCATION"].unique().tolist()[0:14]
    data_of_15_countries_SELFEMPLOYED = df_SELFEMPLOYED[df_SELFEMPLOYED["LOCATION"]
        .isin(countries15_SELFEMPLOYED)]


    chart00 = alt.Chart(data_of_15_countries_TOT, title="Just a raw data")\
        .mark_line().encode(x='TIME', y='Value', color='LOCATION').interactive()

    chart01 = alt.Chart(data_of_15_countries_SELFEMPLOYED, title="Just a raw data")\
        .mark_line().encode(x='TIME', y='Value', color='LOCATION').interactive()

    name = st.text_input("Your name", key="name", value="Anonymous")
    but = st.button("push here if you want to look at a whole DataFrame")
    if but:
        st.write("Here is the full DataFrame: ", df)

    st.write(chart00, chart01)
    print_info(name)

    st.write("Here you can see how many data we have on a particular LOCATION:")
    category = st.selectbox("LOCATION", df["LOCATION"].value_counts().index)
    df_selection = df[lambda x: x["LOCATION"] == category]

    chart = alt.Chart(df_selection, title=f"Number of data of {category}")\
        .mark_bar().encode(x=alt.X('TIME', scale=alt.Scale(domain=[1970, 2018])),
                           y='count()', color='SUBJECT')\
        .configure_legend(fillColor='lightgray', padding=7, cornerRadius=10,
                          orient='top-left').interactive()
    st.write(chart)

    st.text("And here you can also see the proportion of Selfemployed of this data "
            "on selected location and the gap in earnings by the years:")
    fig, ax = plt.subplots(1, 2)
    ax[0].set_title("Share of selfemployed/TOT")

    def get_value_subject(data, subject = "SELFEMPLOYED"):
        try:
            value = data["SUBJECT"].value_counts()[subject]
        except KeyError:
            value = 0
        return value

    values = [get_value_subject(df_selection), get_value_subject(df_selection, "TOT")]
    labels = ["Selfemployed", "TOT"]
    ax[0].pie(values, labels=labels, autopct="%.1f%%")
    ax[1].set_title("Gap values by time")
    df_selection1 = df_selection[df_selection["SUBJECT"]=="TOT"]
    ax[1].plot(df_selection1["TIME"], df_selection1["Value"])
    df_selection2 = df_selection[df_selection["SUBJECT"] == "SELFEMPLOYED"]
    ax[1].plot(df_selection2["TIME"], df_selection2["Value"])
    fig.set_tight_layout(True)
    fig

    def find_all_years(locations):
        times = []
        to_trash = []
        for every_location in locations:
            df1 = df[lambda x: x["LOCATION"] == every_location]
            times.extend(df1["TIME"].unique().tolist())
        times = np.unique(np.array(times))
        for every_location in locations:
            df1 = df[lambda x: x["LOCATION"] == every_location]
            for i in range(len(times)):
                if len(times) <= i:
                    break
                if df1["TIME"].unique().tolist().count(times[i]) == 0:
                    to_trash.append(i)
                    print(times)
        to_trash = np.unique(np.array(to_trash))
        times = np.delete(times, to_trash)
        return times.tolist()

    st.write(f"#### Now, {name}, you can compare the gap values of selected locations "
             f"with particular subject by the time (animation!): ")
    location_choose = df["LOCATION"].unique().tolist()
    subject_choose = df["SUBJECT"].unique().tolist()
    time = df["TIME"].unique().tolist()
    location = st.multiselect("Which locations do you want to compare? You should "
                              "choose at least two", location_choose)
    subject = st.selectbox("Which subject do you want to compare?",
                           df["SUBJECT"].value_counts().index)
    if len(location) > 1:

        gap = df[df["LOCATION"].isin(location)].sort_values(by=['TIME'])
        gap = gap[gap.TIME.isin(find_all_years(location))]
        gap = gap[gap["SUBJECT"] == subject]
        but2 = st.button("push here if you want to look at collected data for "
                         "that comparison")
        if but2:
            st.write("Here is the full DataFrame: ", gap)

        fig2 = px.bar(gap, x='LOCATION', y="Value", color="LOCATION",
                      hover_name="TIME",
                      animation_frame="TIME", animation_group="LOCATION")
        fig2.update_layout(width=1000)
        st.write(fig2)

    st.write(f"#### Here you can see the difference between developed countries "
             f"and developing:")
    Developed_countries = ['AUS', 'AUT', 'BEL', 'CAN', 'CZE', 'DNK', 'FIN', 'FRA',
                           'DEU', 'GRC', 'ISL', 'IRL', 'ITA', 'JPN', 'KOR', 'LUX',
                           'NLD', 'NZL', 'NOR', 'POL', 'PRT', 'SVK', 'ESP', 'SWE',
                           'CHE', 'GBR', 'USA', 'EST', 'ISR', 'SVN', 'LVA', 'LTU',
                           'EU28']
    Developing_countries = ['HUN', 'TUR', 'CHL', 'COL', 'CRI']
    developed = df[df["LOCATION"].isin(Developed_countries)]
    developing = df[df["LOCATION"].isin(Developing_countries)]

    fig3, ax = plt.subplots(1, 2)
    sns.scatterplot(data=developed, x='TIME', y='Value', hue='SUBJECT',
                    style='SUBJECT', palette=['#BB0B4F','#0C35AF'], ax=ax[0])
    ax[0].legend(loc="upper left", fontsize=6)
    sns.scatterplot(data=developing, x='TIME', y='Value', hue="LOCATION",
                    style='SUBJECT',
                    palette=['#BB0B4F', '#EA29C3',
                             '#BD18E4', '#7C18E4', '#0C35AF'],
                    ax=ax[1])
    ax[1].legend(loc="upper left", fontsize=6)
    fig3.set_tight_layout(True)
    st.pyplot(fig3)
    fig4, ax = plt.subplots(1, 2)
    sns.violinplot(x='Value', y='SUBJECT', data=developed,
                   palette=['#BB0B4F', '#0C35AF'],
                   ax=ax[0])
    sns.violinplot(x='Value', y='SUBJECT', data=developing,
                   palette=['#BB0B4F', '#0C35AF'],
                   ax=ax[1])
    fig4.set_tight_layout(True)
    st.pyplot(fig4)

    mean_Value_of_countries = pd.DataFrame(df.groupby('LOCATION')['Value']
                                           .mean()).reset_index()
    brush = alt.selection(type='interval', encodings=['x'])
    bars = alt.Chart().mark_bar(color="#BB0B4F").encode(x='Value', y='LOCATION',
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.2)))\
        .add_selection(brush)

    st.write(f"####And here you finally can choose a range of mean value "
             f"and look at relevant countries(interactivity!):",
             alt.layer(bars, data=mean_Value_of_countries))
