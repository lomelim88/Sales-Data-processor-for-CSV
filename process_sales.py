import pandas as pd
from datetime import datetime
print("Starting Sales Data processor")

#Extract/Read the CSV File
print("n1. Reading CSV File...")
df = pd.read_csv("sales_data.csv")
print(f" Loaded {len(df)} records")

#Transform/Clean the Data
print("n2. Cleaning Data...")

#Show missing values if any
missing_values = df.isnull().sum().sum()
print(f" Missing values: {missing_values}") 

#remove rows with missing values on product row
df = df.dropna(subset=['product'])

#Fill missing customer names with "Unknown"
df['customer'] = df['customer'].fillna("Unknown")

missing_after = df.isnull().sum().sum()
print(f" Missing values after cleaning: {missing_after}")

print("\n3. Calculating Total Sales...")

#Calculate total sales
df['total_amount'] = df['quantity'] * df['price']

#Convert date column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

#Add day of week column
df['day_of_week'] = df['date'].dt.day_name()

print(f" Processed {len(df)} valid records")

#Step 3 Analyze and create summary
print("\n4. Analyzing Data...")

#Total sales by product
total_revenue = df['total_amount'].sum()
print(f" Total Revenue: ${total_revenue:.2f}")

#Sales by product
product_sales = df.groupby('product')['total_amount'].sum().sort_values(ascending=False)
print("\n Sales by Product:")
for product, amount in product_sales.items():
    print(f" {product}: ${amount:.2f}")


#Highest sales customer
customer_sales = df.groupby('customer')['total_amount'].sum().sort_values(ascending=False)
top_customer = customer_sales.idxmax()
top_customer_sales = customer_sales.iloc[0]
print(f"\n Top Customer: {top_customer} with sales of ${top_customer_sales:.2f}")

#Step 4 Load exports the results
print("\n5. Exporting Results...")

#Export cleaned data to new CSV
df.to_csv("cleaned_sales_data.csv", index=False)
print(" Cleaned data exported to cleaned_sales_data.csv")

#export summary report
summary_df = product_sales.reset_index()
summary_df.columns = ['Product', 'Total Sales']
summary_df.to_csv("sales_summary.csv", index=False)
print(" Sales summary exported to sales_summary.csv")

#create text report
with open("sales_report.txt", "w") as report_file:
    report_file.write(f"Sales Report - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_file.write(f"Total Revenue: ${total_revenue:.2f}\n\n")
    report_file.write("Sales by Product:\n")
    for product, amount in product_sales.items():
        report_file.write(f" {product}: ${amount:.2f}\n")
    report_file.write(f"\nTop Customer: {top_customer} with sales of ${top_customer_sales:.2f}\n")
print(" Sales report exported to sales_report.txt")

print("\n Process completed successfully! Please check the output files for results.")