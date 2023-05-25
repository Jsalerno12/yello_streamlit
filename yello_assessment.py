import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Write a query that shows the total number of candidates in the system.
query_1 = "SELECT count(*) num_candidates FROM USERS WHERE user_type = 'candidate';"

# Modify your query to show each candidate in the system, and how many
# unique questions they answered. Sort the result set by the number of
# unique questions answered.

query_2 = '''
    SELECT 
        u.id, 
        u.first_name, 
        u.last_name, 
        COUNT(DISTINCT r.question_id) AS unique_questions_answered
    FROM USERS u
    LEFT JOIN RESPONSES r ON u.id = r.user_id
    WHERE u.user_type = 'candidate'
    GROUP BY u.id, u.first_name, u.last_name
    ORDER BY unique_questions_answered;
'''

# Expand the query to show a flag if the candidate has a resume on file.
query_3 = '''
    SELECT 
        u.id, 
        u.first_name, 
        u.last_name, 
        COUNT(DISTINCT r.question_id) AS unique_questions_answered,
        CASE 
            WHEN d.document_type = 'resume' THEN 'Yes' ELSE 'No' 
        END AS has_resume
    FROM USERS u
    LEFT JOIN RESPONSES r ON u.id = r.user_id
    LEFT JOIN DOCUMENTS d ON u.id = d.user_id AND d.document_type = 'resume'
    WHERE u.user_type = 'candidate'
    GROUP BY u.id, u.first_name, u.last_name, has_resume
    ORDER BY unique_questions_answered;
'''


# Write a query to delete (switch the deleted flag) an admin user if they were
# created prior to [1/1/2020] AND do not have responses to any questions.

query_4 = '''
    UPDATE USERS
    SET deleted = true
    WHERE user_type = 'admin'
        AND created_at < '2020-01-01'
        AND id NOT IN (SELECT DISTINCT user_id FROM RESPONSES);
'''

# Write a query to display the most answered question(s) and how many
# users answered that question(s).

query_5 = '''
    WITH question_responses AS (
        SELECT 
            q.id, 
            q.name AS question_text, 
            count(*) AS num_times_answered,
            COUNT(DISTINCT r.user_id) AS num_distinct_users,
            RANK() OVER (ORDER BY COUNT(*) desc) AS response_count_ranking
        FROM QUESTIONS q
        LEFT JOIN RESPONSES r ON q.id = r.question_id
        GROUP BY q.id, q.name
    )
    SELECT *
    FROM question_responses
    WHERE response_count_ranking = 1;
'''

df_1 = pd.read_sql_query(query_1, conn)
df_2 = pd.read_sql_query(query_2, conn)
df_3 = pd.read_sql_query(query_3, conn)
cursor.executescript(query_4)
df_5 = pd.read_sql_query(query_5, conn)
conn.commit()
conn.close()


fig_2 = px.bar(df_2, x='unique_questions_answered', y='last_name', orientation='h',
               title='Candidates and Unique Questions Answered')
fig_2.update_xaxes(type='category')
fig_3 = px.histogram(df_3, x='unique_questions_answered', y='last_name', color='has_resume',
                     title='Candidate and Resume Availability', orientation='h')


st.set_page_config(layout="wide")
st.title('Yello Report')
st.sidebar.markdown("# About this app")
st.sidebar.markdown("This is a simple app used to display assessment results for Yello. [Github Link](https://github.com/Jsalerno12/yello_streamlit)")

st.header('General Questions')
st.markdown("#### What are the different join types and what do they do?")
st.markdown("Join types in SQL include:")
st.markdown("- Inner Join: Returns only the matching rows between two tables based on the join condition.")
st.markdown("- Left Join: Returns all rows from the left table and the matching rows from the right table.")
st.markdown("- Right Join: Returns all rows from the right table and the matching rows from the left table.")
st.markdown("- Full Outer Join: Returns all rows from both tables, matching rows where available.")
st.markdown("- Cross Join: Returns the Cartesian product of both tables, resulting in all possible combinations.")

st.markdown("#### What is an index and why/when do you use them?")
st.markdown("An index is a db structure that improves the speed of data retrieval operations on a table. It enables \
            faster lookup time of rows based on a specific column or group of columns. They are generally used to \
            help optimize query performance by reducing the number of i/o operations required.")

st.markdown("#### What is a view and when might you use it?")
st.markdown("A view is a virtual table created from the result of a query. It allows you to store a pre-defined \
            query as one of these virtual tables and use it in subsequent queries. Views provide a way to simplify complex queries by \
            hiding the underlying complexity of data models. For instance, there may be a specific set of facts that analysts consistently need to use. \
            If this data is normally retrieved by combining numerous other tables with complex join logic, it may make sense to create a view to reduce \
            this complexity. They can also be used to provide controlled access to data for different users or applications.")

st.markdown("#### Difference between CTE and Subquery? Provide an example of when you would use one or the other.")
st.markdown("CTE (Common Table Expression) and subqueries are both used to create temporary result sets.")
st.markdown("- CTE is a named temporary result set that can be referenced multiple times in a query. CTEs are great for enhancing code readability, reusability, and testability.")
st.markdown("- Subquery is a query nested inside another query and can only be referenced at the specific location it is defined. There are both correlated and un-correlated subqueries.")
st.markdown("Generally, I would use a subquery if the temporary result set is simple and does not need to be referenced multiple times. This might look like SELECT user_id FROM users WHERE user_id IN (SELECT user_id FROM responses WHERE response_date > '2023-01-01')")
st.markdown("CTEs would be used when they the logic is relatively complex, and it needs to be used in further joins or operations throughout the query.")

st.markdown("#### Used functions/stored procedures before? Provide an example of how you used either before.")
st.markdown("Yes, I've used them many times, most frequently with dbt. For instance, one procedure I created recently was for recreating test datasets. \
            This script provides the user a set of variables to set as parameters: project_id, dataset, etc. It then runs a series of safety checks \
            to verify the user is performing operations in the correct tables and verifies the tables are empty. It then executes a series of drop and \
            create schema commands to generate the new tables and datasets. An example of a simple function I created took in as input a lat/long tuple for both a origin and destination, and returned the total distance traveled in km. This was created in dbt using jinja.")
st.markdown("#### How might you approach optimizing a slow performing query?")
st.markdown("There are a large number of ways we might approach a slow performing query depending on the needs of whoever/whatever is using it. ")
st.markdown("- The first step would be to benchmark the queries performance to determine whether it's actually a slowly performing query, or if it was just being run during a period of particularly high load on the db, resulting in slower processing times.")
st.markdown("- If the issue is not with db load itself, the next step would be to visually review the query. This would include looking for things like: inefficient joins that join huge amounts of unecessary data, or result in cartesian products. \
            Retrieving too much data in general (using select * statements, or not using where clauses to limit result sets). Reducing the number of sub-queries if there are too many unecessarily added in the query.")
st.markdown("- The next step may be to analyze the query explain plan to determine which sections of the query are taking the bulk of the time. This enables you to laser in on high cost operations, missing indexes, or full table scans.")
st.markdown("- If the query itself can't be improved, we may determine that an index is necessary to improve load times.")
st.markdown("- Last, it might be necessary to cache the data in some way. An example of this would be a materialized view.")

# Total Number of Candidates
st.header('Total Number of Candidates')
st.code(query_1)
total_candidates = df_1['num_candidates'].iloc[0]
st.write(f"The total number of candidates in the system is: {total_candidates}")

# Candidates and Unique Questions Answered
st.header('Candidates and Unique Questions Answered')
st.code(query_2)
st.dataframe(df_2)

# Plot: Candidates and Unique Questions Answered
st.plotly_chart(fig_2, use_container_width=True)

# Candidates and Resume Availability
st.header('Candidates Unique Questions Answered and Resume Availability')
st.code(query_3)
st.dataframe(df_3)

# Plot: Candidates and Resume Availability
st.plotly_chart(fig_3, use_container_width=True)

# Deleted Admin Users
st.header('Deleted Admin Users')
st.code(query_4)
st.write("Admin users created prior to 1/1/2020 and without responses have been deleted.")

# Most Answered Question(s)
st.header('Most Answered Question(s)')
st.code(query_5)
st.dataframe(df_5)