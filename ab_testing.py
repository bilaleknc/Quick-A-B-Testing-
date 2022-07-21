

def CompareTwoGroups(dataframe1, dataframe2, col):
    # 1. Normality Test: Shapiro Test
    # 2. Homogeneity Test: Levene Test
    # 3. Parametric or Non-Parametric T Test: T-Test, Welch Test, Mann Whitney U
    groupA = dataframe1[col]
    groupB = dataframe2[col]

    norm1 = shapiro(groupA)[1] < 0.05
    norm2 = shapiro(groupB)[1] < 0.05
    # H0: Distribution is Normal! - False
    # H1: Distribution is not Normal! - True

    if (norm1 == False) & (norm2 == False):  # "H0: Normal Distribution"
        # Parametric Test
        # Assumption: Homogeneity of variances
        leveneTest = levene(groupA, groupB)[1] < 0.05
        # H0: Homogeneity: False
        # H1: Heterogeneous: True
        if leveneTest == False:
            # Homogeneity
            ttest = ttest_ind(groupA, groupB, equal_var=True)[1]
            # H0: M1 = M2 - False
            # H1: M1 != M2 - True
        else:
            # Heterogeneous
            ttest = ttest_ind(groupA, groupB, equal_var=False)[1]
            # H0: M1 = M2 - False
            # H1: M1 != M2 - True
    else:
        # Non-Parametric Test
        ttest = mannwhitneyu(groupA, groupB)[1]
        # H0: M1 = M2 - False
        # H1: M1 != M2 - True

    temp = pd.DataFrame({"Compare Two Groups": [ttest < 0.05],
                         "p-value": [ttest],
                         "GroupA_Mean": [groupA.mean()], "GroupB_Mean": [groupB.mean()],
                         "GroupA_Median": [groupA.median()], "GroupB_Median": [groupB.median()],
                         "GroupA_Count": [groupA.count()], "GroupB_Count": [groupB.count()]
                         })
    temp["Compare Two Groups"] = np.where(temp["Compare Two Groups"] == True, "Different Groups", "Similar Groups")
    temp["TestType"] = np.where((norm1 == False) & (norm2 == False), "Parametric", "Non-Parametric")
    AB = pd.DataFrame()
    AB = pd.concat([AB, temp[["TestType", "Compare Two Groups", "p-value", "GroupA_Median", "GroupB_Median", "GroupA_Mean",
                              "GroupB_Mean",
                              "GroupA_Count", "GroupB_Count"]]])

    return AB


AB = CompareTwoGroups(Test_Group, Control_Group, "Purchase")
AB = CompareTwoGroups(Control_Group, Test_Group, "Earning")
