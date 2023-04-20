import csv
import matplotlib.pyplot as plt
import numpy as np

skills = ["team", "statistics", "software", "research", "python", "model", "machine learning", "analyse"]
salary_bands = {'Less than $50,000': (0, 50000),
                '$50,000 - $59,999': (50000, 60000),
                '$60,000 - $69,999': (60000, 70000),
                '$70,000 - $79,999': (70000, 80000),
                '$80,000 - $89,999': (80000, 90000),
                '$90,000 - $99,999': (90000, 100000),
                '$100,000 - $124,999': (100000, 125000),
                '$125,000 - $149,999': (125000, 150000),
                'Above $150,000': (150000, float('inf'))}

job_skills = {}  # dictionary to store the frequency of skills by job title
salary_counts = {}  # dictionary to store the frequency of skills by salary band


with open('Cleaned_DS_Jobs.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # skip the header row
    for row in reader:
        job_title = row[0]
        salary_estimate = row[1]
        job_description = row[2]
        salary_estimate = salary_estimate.replace(" (Glassdoor est.)", "")
        salary_estimate = salary_estimate.replace("K", "")
        salary_estimate = salary_estimate.replace("$", "")
        salary_estimate = salary_estimate.replace("-", " ")
        parts = salary_estimate.split()
        salary_min = int(parts[0]) * 1000
        salary_max = int(parts[1]) * 1000
        salary_covered = set()
        for band, (min_salary, max_salary) in salary_bands.items():
            if salary_min <= max_salary and salary_max >= min_salary:
                salary_covered.add(band)
        for skill in skills:
            if skill.lower() in job_description.lower():
                if job_title in job_skills:
                    job_skills[job_title][skill] = job_skills[job_title].get(skill, 0) + 1
                else:
                    job_skills[job_title] = {skill: 1}
                if salary_covered:  # only count into salary bands when at least one salary band is covered
                    for band in salary_covered:
                        if band in salary_counts:
                            salary_counts[band][skill] = salary_counts[band].get(skill, 0) + 1
                        else:
                            salary_counts[band] = {skill: 1}

"""
print("\nSkill frequencies by salary band:")
for band, salary_range in salary_bands.items():
    print(f"{band}:")
    for skill, frequency in salary_counts[band].items():
        print(f"\t{skill}: {frequency}")
"""

# Set up the color palette
color_palette = {
    "team": "#1f77b4",
    "statistics": "#ff7f0e",
    "software": "#2ca02c",
    "research": "#d62728",
    "python": "#9467bd",
    "model": "#8c564b",
    "machine learning": "#e377c2",
    "analyse": "#7f7f7f"
}

# Sort skills based on the order of keys in color_palette dictionary
skills = sorted(skills, key=lambda x: list(color_palette.keys()).index(x))
# Create a dictionary to store the skill counts for each salary band
skill_counts_by_band = {band: {skill: 0 for skill in skills} for band in salary_bands}

# Aggregate the skill counts for each salary band
for band, skills in salary_counts.items():
    for skill, count in skills.items():
        skill_counts_by_band[band][skill] += count

# Prepare the data for plotting
x = list(salary_bands.keys())
y = [list(skill_counts_by_band[band].values()) for band in salary_bands]

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_title('Skill Frequencies by Salary Band (Data Scientist)')
ax.set_ylabel('Frequency')
ax.set_xlabel('Salary band')

# Plot each skill as a separate line
for i, skill in enumerate(color_palette.keys()):
    ax.plot(x, [y[j][i] for j in range(len(y))], marker='o', color=color_palette[skill], label=skill)
ax.legend(loc='best')

plt.grid(True)
plt.show()

# Calculate total skill frequency for each salary band
salary_totals = {}
for band, skills in salary_counts.items():
    salary_totals[band] = sum(skills.values())

# Calculate skill frequencies as a percentage of total frequency for each salary band
skill_percentages = {}
for band, skills in salary_counts.items():
    percentages = []
    for skill, frequency in skills.items():
        percentage = round((frequency / salary_totals[band]) * 100, 2)
        percentages.append(percentage)
    skill_percentages[band] = percentages

# Create line chart for each skill
fig, axs = plt.subplots(1, 1, figsize=(10, 8))
salary_band_names = [band for band, salary_range in salary_bands.items()]

for i, skill in enumerate(color_palette.keys()):
    axs.plot(salary_band_names, [percentages[i] for percentages in skill_percentages.values() for i, s in enumerate(skills) if s == skill], marker='o', color=color_palette[skill], label=skill)

axs.set_xlabel('Salary Band')
axs.set_ylabel('Percentage')
axs.set_title('Skill Percentages by Salary Band (Data Scientist)')
axs.legend(loc='upper center', bbox_to_anchor=(1.06, 0.5))
plt.grid(True)
plt.show()
