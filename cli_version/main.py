import pandas as pd
import numpy as np

# Step 1: Load and clean the data
def load_bank_data(filepath):
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')
    return df

# Step 2: Filter only withdrawals
def get_withdrawals_only(df):
    df_filtered = df[df['withdrawals'] != ""]
    df_filtered['withdrawals'] = df_filtered['withdrawals'].astype(float)
    return df_filtered

# Step 3: Show most frequent merchants
def show_frequent_merchants(df_filtered, top_n=10):
    merchant_counts = df_filtered['description'].value_counts().head(top_n)
    print("\nMost Frequent Withdrawal Descriptions:")
    print(merchant_counts)

# Step 4: Detect possible subscriptions
def detect_recurring_subscriptions(df_filtered, min_months=3):
    recurring = []

    # Group by merchant (description)
    for name, group in df_filtered.groupby('description'):
        group = group.sort_values(by='date')

        # Convert date to month-year format
        months = group['date'].dt.to_period('M').unique()
        avg_amount = np.mean(group['withdrawals'])

        if len(months) >= min_months:
            recurring.append({
                'Merchant': name,
                'Occurrences': len(group),
                'Months Active': len(months),
                'Average Amount': round(avg_amount, 2)
            })

    return pd.DataFrame(recurring).sort_values(by='Months Active', ascending=False)

# Step 5: Main runner
if __name__ == "__main__":
    path = 'sample_data/Canadian_Bank_Statement.csv'
    data = load_bank_data(path)

    withdrawals = get_withdrawals_only(data)
    show_frequent_merchants(withdrawals)

    print("\nPossible Recurring Subscriptions:")
    subscriptions = detect_recurring_subscriptions(withdrawals)
    print(subscriptions.head(10))
