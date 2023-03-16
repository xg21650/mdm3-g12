# define salary bands
salary_bands = {'Less than $50,000': (0, 50000),
                '$50,000 - $59,999': (50000, 60000),
                '$60,000 - $69,999': (60000, 70000),
                '$70,000 - $79,999': (70000, 80000),
                '$80,000 - $89,999': (80000, 90000),
                '$90,000 - $99,999': (90000, 100000),
                '$100,000 - $124,999': (100000, 125000),
                '$125,000 - $149,999': (125000, 150000),
                'Above $150,000': (150000, float('inf'))}

# define skills
skills = ["Python", "SQL", "Excel", "data analysis", "statistics", "data visualization"]

# initialize frequency count dictionaries for skills and salary bands
skill_freq = {skill: 0 for skill in skills}
salary_band_freq = {salary_band: 0 for salary_band in salary_bands}

# read csv file and extract information
with open('DataAnalyst.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    # loop over rows
    for line in lines[1:]:
        row = line.strip().split(',')
        # extract job title, salary estimate, and job description
        job_title = row[2]
        salary_estimate = row[3]
        job_description = row[4]
        # categorize salary estimate into salary bands
        salary_estimate_range = salary_estimate.split()[0]
        salary_estimate_range = salary_estimate_range.replace('(Glassdoor est.)', '')
        salary_estimate_min = int(salary_estimate_range.split('-')[0].replace('$', '').replace('K', '')) * 1000
        salary_estimate_max = int(salary_estimate_range.split('-')[1].replace('$', '').replace('K', '')) * 1000
        salary_estimate_avg = (salary_estimate_min + salary_estimate_max) / 2
        salary_estimate_band = None
        for band, (lower, upper) in salary_bands.items():
            if lower <= salary_estimate_avg < upper:
                salary_estimate_band = band
                break
        # count skills and salary bands for job title
        for skill in skills:
            if skill.lower() in job_description.lower():
                skill_freq[skill] += 1
                salary_band_freq[salary_estimate_band] += 1

# print skill frequencies by salary band
for band, (lower, upper) in salary_bands.items():
    print(f"Salary band: {band}")
    print(f"Skill frequencies: {skill_freq}")
    print(f"Total jobs in salary band: {salary_band_freq[band]}")
    print()

# print skill frequencies by job title
job_title_freq = {job_title: {skill: 0 for skill in skills} for job_title in set(job_titles)}
for i, job_title in enumerate(job_titles):
    for skill in skills:
        if skill.lower() in job_descriptions[i].lower():
            job_title_freq[job_title][skill] += 1
print("Skill frequencies by job title:")
for job_title, skill_freq in job_title_freq.items():
    print(f"Job title: {job_title}")
    print(f"Skill frequencies: {skill_freq}")
    print()
