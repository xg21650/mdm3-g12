import csv

skills = ["Python", "SQL", "Excel", "data analysis", "statistics", "data visualization"]
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


with open('DataAnalyst.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # skip the header row
    for row in reader:
        job_title = row[1]
        salary_estimate = row[2]
        job_description = row[3]
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


# Print the results
print("Skill frequencies by job title:")
for title, skills in job_skills.items():
    print(f"{title}: {skills}")

print("\nSkill frequencies by salary band:")
for band, skills in salary_counts.items():
    print(f"{band}:")
    for skill, frequency in skills.items():
        print(f"\t{skill}: {frequency}")

