#!/usr/bin/env python
# coding: utf-8

# # v.jahnavi

# # 2211cs010583

# # group3

# In[18]:


import pandas as pd
df=pd.read_csv("srfclftDsttab5.14 (2).csv")
df


# In[5]:


import sqlite3
import pandas as pd


# In[6]:


# Load the dataset
df = pd.read_csv("srfclftDsttab5.14 (2).csv")

# Display the first few rows
df.head()


# In[7]:


# Connect to SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect("irrigation_data.db")
cursor = conn.cursor()

# Save the DataFrame to the SQL database
df.to_sql("irrigation_data", conn, if_exists="replace", index=False)
print("Data loaded into SQLite successfully!")


# In[8]:


query = "SELECT * FROM irrigation_data LIMIT 5;"
df_sql = pd.read_sql(query, conn)
df_sql


# In[9]:


query = """
SELECT State, SUM(Total) AS Total_Irrigation
FROM irrigation_data
GROUP BY State
ORDER BY Total_Irrigation DESC;
"""
df_sql = pd.read_sql(query, conn)
df_sql


# In[11]:


query = """
SELECT State, SUM(Total) AS Total_Irrigation
FROM irrigation_data
GROUP BY State
ORDER BY Total_Irrigation DESC
LIMIT 5;
"""
df_sql = pd.read_sql(query, conn)
df_sql


# In[12]:


query = """
SELECT State, SUM(Total) AS Total_Irrigation
FROM irrigation_data
GROUP BY State
ORDER BY Total_Irrigation ASC
LIMIT 5;
"""
df_sql = pd.read_sql(query, conn)
df_sql


# In[13]:


query = """
SELECT District, State
FROM irrigation_data
WHERE Total = 0;
"""
df_sql = pd.read_sql(query, conn)
df_sql


# In[14]:


query = """
SELECT District, State, Total,
       RANK() OVER (ORDER BY Total DESC) AS Rank_Irrigation
FROM irrigation_data;
"""
df_sql = pd.read_sql(query, conn)
df_sql


# In[16]:


conn.close()
print("Database connection closed.")


# In[19]:


# Group by State and sum the Total irrigation
statewise_irrigation = df.groupby("State")["Total"].sum().reset_index()

# Display top states with highest irrigation
statewise_irrigation.sort_values(by="Total", ascending=False).head()


# In[20]:


import matplotlib.pyplot as plt
import seaborn as sns


top_states = statewise_irrigation.sort_values(by="Total", ascending=False).head(10)

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(x="Total", y="State", data=top_states, palette="Blues_r")
plt.xlabel("Total Irrigation Area")
plt.ylabel("State")
plt.title("Top 10 States by Irrigation Area")
plt.show()


# In[21]:


# Summing up all types of irrigation
irrigation_types = df.iloc[:, 2:-1].sum()

# Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(irrigation_types, labels=irrigation_types.index, autopct="%1.1f%%", colors=sns.color_palette("pastel"))
plt.title("Distribution of Irrigation Types Across India")
plt.show()


# In[22]:


# Correlation matrix
plt.figure(figsize=(8,6))
sns.heatmap(df.iloc[:, 2:].corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Between Irrigation Types")
plt.show()


# In[24]:


plt.figure(figsize=(10, 6))
sns.scatterplot(x=df["Actual area irrigated - Kharif"], y=df["Actual area irrigated - Rabi"], hue=df["State"], alpha=0.7)
plt.xlabel("Kharif Irrigation Area")
plt.ylabel("Rabi Irrigation Area")
plt.title("Scatter Plot: Kharif vs Rabi Irrigation")
plt.legend([],[], frameon=False)  # Hides excessive legend entries
plt.show()


# In[25]:


plt.figure(figsize=(12, 6))
sns.stripplot(y="State", x="Total", data=df, jitter=True, palette="viridis", alpha=0.7)
plt.xlabel("Total Irrigation Area")
plt.ylabel("State")
plt.title("Dot Plot of Irrigation Distribution Across States")
plt.show()


# In[27]:


top_districts = df.groupby("District")["Total"].sum().reset_index().sort_values(by="Total", ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x="Total", y="District", data=top_districts, palette="magma")
plt.xlabel("Total Irrigation Area")
plt.ylabel("District")
plt.title("Top 10 Districts by Irrigation Area")
plt.show()


# In[28]:


state_avg_irrigation = df.groupby("State")["Total"].mean().reset_index().sort_values(by="Total", ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x="Total", y="State", data=state_avg_irrigation, palette="viridis")
plt.xlabel("Average Irrigation Per District")
plt.ylabel("State")
plt.title("State-wise Average Irrigation Per District")
plt.show()


# In[30]:


plt.figure(figsize=(10, 6))
sns.scatterplot(x=df["Total"], y=df["Actual area irrigated - Others"], alpha=0.6, color="red")
plt.xlabel("Total Irrigation Area")
plt.ylabel("Other Irrigation Area")
plt.title("Scatter Plot: Total vs Other Irrigation")
plt.show()


# In[31]:


plt.figure(figsize=(12, 6))
sns.boxplot(x="State", y="Total", data=df, palette="pastel")
plt.xticks(rotation=90)
plt.xlabel("State")
plt.ylabel("Total Irrigation Area")
plt.title("Box Plot: Total Irrigation Distribution Across States")
plt.show()


# In[32]:


plt.figure(figsize=(12, 6))
df_melted = df.melt(id_vars=["State"], value_vars=["Actual area irrigated - Kharif", "Actual area irrigated - Rabi", 
                                                     "Actual area irrigated - Perennial", "Actual area irrigated - Others"],
                    var_name="Irrigation Type", value_name="Irrigation Area")
sns.boxplot(x="Irrigation Type", y="Irrigation Area", data=df_melted, palette="coolwarm")
plt.xlabel("Irrigation Type")
plt.ylabel("Irrigation Area")
plt.title("Box Plot: Distribution of Irrigation Types Across States")
plt.show()


# In[33]:


plt.figure(figsize=(12, 6))
sns.histplot(df["Actual area irrigated - Kharif"], bins=20, kde=True, color="blue", label="Kharif", alpha=0.6)
sns.histplot(df["Actual area irrigated - Rabi"], bins=20, kde=True, color="red", label="Rabi", alpha=0.6)
sns.histplot(df["Actual area irrigated - Perennial"], bins=20, kde=True, color="green", label="Perennial", alpha=0.6)
sns.histplot(df["Actual area irrigated - Others"], bins=20, kde=True, color="purple", label="Others", alpha=0.6)
plt.xlabel("Irrigation Area")
plt.ylabel("Frequency")
plt.title("Histogram: Distribution of Irrigation Types")
plt.legend()
plt.show()


# In[34]:


plt.figure(figsize=(10, 6))
plt.hist(df["Total"], bins=20, color="blue", edgecolor="black", alpha=0.7)
plt.xlabel("Total Irrigation Area")
plt.ylabel("Frequency")
plt.title("Histogram: Distribution of Total Irrigation")
plt.show()


# In[35]:


plt.figure(figsize=(10, 6))
plt.hist(df["Actual area irrigated - Rabi"], bins=20, color="green", edgecolor="black", alpha=0.7)
plt.xlabel("Rabi Irrigation Area")
plt.ylabel("Frequency")
plt.title("Histogram: Distribution of Rabi Irrigation")
plt.show()


# In[36]:


plt.figure(figsize=(12, 6))
plt.hist(df["Actual area irrigated - Kharif"], bins=20, color="blue", alpha=0.5, label="Kharif", edgecolor="black")
plt.hist(df["Actual area irrigated - Rabi"], bins=20, color="red", alpha=0.5, label="Rabi", edgecolor="black")
plt.hist(df["Actual area irrigated - Perennial"], bins=20, color="green", alpha=0.5, label="Perennial", edgecolor="black")
plt.hist(df["Actual area irrigated - Others"], bins=20, color="purple", alpha=0.5, label="Others", edgecolor="black")
plt.xlabel("Irrigation Area")
plt.ylabel("Frequency")
plt.title("Histogram: Comparison of Different Irrigation Types")
plt.legend()
plt.show()


# In[37]:


# Get top 5 districts
top_districts = df.groupby("District")["Total"].sum().sort_values(ascending=False).head(5)

# Plot
plt.figure(figsize=(8, 8))
plt.pie(top_districts, labels=top_districts.index, autopct="%1.1f%%", colors=plt.cm.Accent.colors)
plt.title("Top 5 Districts by Total Irrigation")
plt.show()


# In[38]:


# Get top 5 states
top_states = df.groupby("State")["Total"].sum().sort_values(ascending=False).head(5)

# Plot
plt.figure(figsize=(8, 8))
plt.pie(top_states, labels=top_states.index, autopct="%1.1f%%", colors=plt.cm.Set3.colors)
plt.title("Top 5 States by Total Irrigation")
plt.show()


# In[ ]:




