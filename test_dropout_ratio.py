"""
Clinical Trial Patient Dropout Ratio Analysis

Calculate overall and treatment-arm-specific dropout rates based on CDISC Pilot 01 data.
"""

import pandas as pd
import numpy as np
import sys
import io

# Set UTF-8 encoding for Windows compatibility
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def calculate_dropout_ratio(data_path='data/model_dataset.csv'):
    """
    Calculate dropout ratio

    Parameters:
    -----------
    data_path : str
        Path to model_dataset.csv file

    Returns:
    --------
    dict : Overall and arm-specific dropout ratios
    """
    # Load data
    df = pd.read_csv(data_path)

    # Overall dropout ratio
    total_patients = len(df)
    total_dropouts = int(df['DROPOUT'].sum())
    total_completed = total_patients - total_dropouts
    overall_dropout_rate = (total_dropouts / total_patients) * 100

    print("=" * 60)
    print("[Clinical Trial Dropout Analysis]")
    print("=" * 60)
    print(f"\nTotal Patients: {total_patients}")
    print(f"Completed: {total_completed} ({100 - overall_dropout_rate:.1f}%)")
    print(f"Dropout: {total_dropouts} ({overall_dropout_rate:.1f}%)")
    print("\n" + "-" * 60)

    # Dropout ratio by treatment arm
    print("\nDropout Ratio by Treatment Arm:")
    print("-" * 60)

    results = {
        'overall': {
            'total': total_patients,
            'completed': total_completed,
            'dropout': total_dropouts,
            'dropout_rate': overall_dropout_rate
        }
    }

    arms = {
        'Placebo': 'ARM_PLACEBO',
        'Xanomeline Low Dose': 'ARM_LOW',
        'Xanomeline High Dose': 'ARM_HIGH'
    }

    for arm_name, arm_col in arms.items():
        # Filter patients in this arm
        arm_df = df[df[arm_col] == 1]
        arm_total = len(arm_df)
        arm_dropouts = int(arm_df['DROPOUT'].sum())
        arm_completed = arm_total - arm_dropouts
        arm_dropout_rate = (arm_dropouts / arm_total) * 100 if arm_total > 0 else 0

        print(f"\n{arm_name:25s}")
        print(f"  Total: {arm_total:3d} patients")
        print(f"  Completed: {arm_completed:3d} ({100 - arm_dropout_rate:.1f}%)")
        print(f"  Dropout: {arm_dropouts:3d} ({arm_dropout_rate:.1f}%)")

        results[arm_name] = {
            'total': arm_total,
            'completed': arm_completed,
            'dropout': arm_dropouts,
            'dropout_rate': arm_dropout_rate
        }

    print("\n" + "=" * 60)

    return results


def create_dropout_summary_table(results):
    """
    Create dropout ratio summary table

    Parameters:
    -----------
    results : dict
        Return value from calculate_dropout_ratio()

    Returns:
    --------
    pd.DataFrame : Summary table
    """
    summary_data = []

    for arm_name, stats in results.items():
        if arm_name != 'overall':
            summary_data.append({
                'Treatment Arm': arm_name,
                'Total': stats['total'],
                'Completed': stats['completed'],
                'Dropout': stats['dropout'],
                'Dropout Rate(%)': round(stats['dropout_rate'], 1)
            })

    summary_df = pd.DataFrame(summary_data)

    print("\n[Summary Table]")
    print(summary_df.to_string(index=False))

    return summary_df


def analyze_dropout_by_features(data_path='data/model_dataset.csv', top_n=5):
    """
    Analyze dropout ratio by key features

    Parameters:
    -----------
    data_path : str
        Path to model_dataset.csv file
    top_n : int
        Number of top features to display
    """
    df = pd.read_csv(data_path)

    print("\n" + "=" * 60)
    print("[Feature-based Dropout Analysis]")
    print("=" * 60)

    # By Gender (SEX_N: 0=Female, 1=Male)
    print("\n[By Gender]")
    for sex in [0, 1]:
        sex_df = df[df['SEX_N'] == sex]
        sex_name = "Female" if sex == 0 else "Male"
        dropout_rate = (sex_df['DROPOUT'].sum() / len(sex_df)) * 100
        print(f"  {sex_name}: {dropout_rate:.1f}% ({int(sex_df['DROPOUT'].sum())}/{len(sex_df)})")

    # By SAE (Serious Adverse Event)
    print("\n[By SAE (Serious Adverse Event)]")
    for sae in [0, 1]:
        sae_df = df[df['HAS_SAE'] == sae]
        sae_name = "No SAE" if sae == 0 else "Has SAE"
        dropout_rate = (sae_df['DROPOUT'].sum() / len(sae_df)) * 100 if len(sae_df) > 0 else 0
        print(f"  {sae_name}: {dropout_rate:.1f}% ({int(sae_df['DROPOUT'].sum())}/{len(sae_df)})")

    # By Age Group
    print("\n[By Age Group]")
    df['AGE_GROUP'] = pd.cut(df['AGE'], bins=[0, 65, 75, 100], labels=['<= 65', '66-75', '76+'])
    for age_group in df['AGE_GROUP'].cat.categories:
        age_df = df[df['AGE_GROUP'] == age_group]
        if len(age_df) > 0:
            dropout_rate = (age_df['DROPOUT'].sum() / len(age_df)) * 100
            print(f"  {age_group}: {dropout_rate:.1f}% ({int(age_df['DROPOUT'].sum())}/{len(age_df)})")

    # By AE Count quartiles
    print("\n[By AE (Adverse Event) Count]")
    df['AE_QUARTILE'] = pd.qcut(df['AE_COUNT'], q=4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'], duplicates='drop')
    for quartile in df['AE_QUARTILE'].cat.categories:
        ae_df = df[df['AE_QUARTILE'] == quartile]
        if len(ae_df) > 0:
            dropout_rate = (ae_df['DROPOUT'].sum() / len(ae_df)) * 100
            ae_range = f"({ae_df['AE_COUNT'].min():.0f}-{ae_df['AE_COUNT'].max():.0f})"
            print(f"  {quartile} {ae_range}: {dropout_rate:.1f}% ({int(ae_df['DROPOUT'].sum())}/{len(ae_df)})")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("\nStarting Clinical Trial Dropout Analysis...\n")

    # 1. Calculate dropout ratio
    results = calculate_dropout_ratio()

    # 2. Create summary table
    summary_df = create_dropout_summary_table(results)

    # 3. Analyze dropout by features
    analyze_dropout_by_features()

    print("\n[Analysis Complete!]\n")
