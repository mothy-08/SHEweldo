document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        document.querySelector(".formSalary").classList.add("show");
    }, 100);
});

async function populateCompanies() {
    try {
        const response = await fetch("/api/companies");
        const companies = await response.json();
        const filter = document.getElementById("company");

        companies.sort((a, b) => a.name.localeCompare(b.name));
        companies.forEach((company) => {
            const option = document.createElement("option");
            option.value = company.hash;
            option.textContent = company.name;
            filter.appendChild(option);
        });
    } catch (error) {
        console.error("Error loading companies:", error);
    }
}

function populateDepartments() {
    const departments = [
        "executive_leadership",
        "operations",
        "finance_accounting",
        "human_resources",
        "legal_compliance",
        "marketing_sales",
        "customer_service_support",
        "technology_it",
        "product_rd",
        "supply_chain_logistics",
        "other",
    ];
    const filter = document.getElementById("department");
    departments.forEach((dept) => {
        const option = document.createElement("option");
        option.value = dept;
        option.textContent = dept
            .split("_")
            .map((word) => word[0].toUpperCase() + word.slice(1))
            .join(" ");
        filter.appendChild(option);
    });
}

document.addEventListener("DOMContentLoaded", populateDepartments);

document.addEventListener("DOMContentLoaded", populateCompanies);

document.getElementById("addCompanyBtn").addEventListener("click", () => {
    window.location.href = "/company/submit";
});

document.getElementById("salaryForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const companyHash = document.getElementById("company").value;
    const yearsAtCompany = parseInt(document.getElementById("years_at_the_company").value);
    const totalExperience = parseInt(document.getElementById("total_experience").value);
    const salaryAmount = parseFloat(document.getElementById("salary_amount").value);
    const gender = document.getElementById("gender").value;
    const department = document.getElementById("department").value;
    const jobTitle = document.getElementById("job_title").value;

    const messageDiv = document.getElementById("message");

    if (!companyHash) {
        messageDiv.style.display = "block";
        messageDiv.style.backgroundColor = "#f8d7da";
        messageDiv.style.color = "#721c24";
        messageDiv.textContent = "Please select a company.";
        return;
    }

    if (isNaN(yearsAtCompany) || yearsAtCompany < 0 || yearsAtCompany > 50) {
        messageDiv.style.display = "block";
        messageDiv.style.backgroundColor = "#f8d7da";
        messageDiv.style.color = "#721c24";
        messageDiv.textContent = "Years at company must be between 0 and 50.";
        return;
    }

    if (isNaN(totalExperience) || totalExperience < 0 || totalExperience > 50) {
        messageDiv.style.display = "block";
        messageDiv.style.backgroundColor = "#f8d7da";
        messageDiv.style.color = "#721c24";
        messageDiv.textContent = "Total experience must be between 0 and 50.";
        return;
    }

    if (totalExperience < yearsAtCompany) {
        messageDiv.style.display = "block";
        messageDiv.style.backgroundColor = "#f8d7da";
        messageDiv.style.color = "#721c24";
        messageDiv.textContent = "Total experience must be greater than or equal to years at the company.";
        return;
    }

    if (isNaN(salaryAmount) || salaryAmount < 0) {
        messageDiv.style.display = "block";
        messageDiv.style.backgroundColor = "#f8d7da";
        messageDiv.style.color = "#721c24";
        messageDiv.textContent = "Salary amount must be a positive number.";
        return;
    }

    if (!gender) {
        messageDiv.style.display = "block";
        messageDiv.style.backgroundColor = "#f8d7da";
        messageDiv.style.color = "#721c24";
        messageDiv.textContent = "Please select a gender.";
        return;
    }

    if (!department) {
        messageDiv.style.display = "block";
        messageDiv.style.backgroundColor = "#f8d7da";
        messageDiv.style.color = "#721c24";
        messageDiv.textContent = "Please select a department.";
        return;
    }

    if (!jobTitle) {
        messageDiv.style.display = "block";
        messageDiv.style.backgroundColor = "#f8d7da";
        messageDiv.style.color = "#721c24";
        messageDiv.textContent = "Please enter a job title.";
        return;
    }

    const formData = {
        company_hash: companyHash,
        years_at_the_company: yearsAtCompany,
        total_experience: totalExperience,
        salary_amount: salaryAmount,
        gender: gender,
        submission_date: new Date().toISOString().split("T")[0],
        is_well_compensated: document.getElementById("is_well_compensated").value === "true",
        department: department,
        job_title: jobTitle,
    };

    try {
        const response = await fetch("/api/employee/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        });

        const result = await response.json();

        if (response.ok) {
            messageDiv.style.display = "block";
            messageDiv.style.backgroundColor = "#d4edda";
            messageDiv.style.color = "#155724";
            messageDiv.textContent = "Submission successful! Thank you for your contribution.";
            document.getElementById("salaryForm").reset();

            setTimeout(() => {
                window.location.href = "/employee/graph";
            }, 500);
        } else {
            messageDiv.style.display = "block";
            messageDiv.style.backgroundColor = "#f8d7da";
            messageDiv.style.color = "#721c24";
            messageDiv.textContent = result.error || "Error submitting salary data";
        }

        setTimeout(() => {
            messageDiv.style.display = "none";
        }, 5000);
    } catch (error) {
        console.error("Error:", error);
        messageDiv.style.display = "block";
        messageDiv.style.backgroundColor = "#f8d7da";
        messageDiv.style.color = "#721c24";
        messageDiv.textContent = "Network error - please try again later.";
    }
});