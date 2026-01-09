import pandas as pd
import numpy as np

def run_detector(filepath):
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['withdrawals'] != ""]
    df['withdrawals'] = df['withdrawals'].astype(float)

    recurring = []

    for name, group in df.groupby('description'):
        group = group.sort_values(by='date')
        months = group['date'].dt.to_period('M').unique()
        avg_amount = np.mean(group['withdrawals'])

        if len(months) >= 3:
            recurring.append({
                'Merchant': name,
                'Occurrences': len(group),
                'Months Active': len(months),
                'Average Amount': round(avg_amount, 2)
            })

    return pd.DataFrame(recurring).sort_values(by='Months Active', ascending=False)