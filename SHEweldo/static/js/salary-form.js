
async function populateCompanies() {
    try {
        const response = await fetch('/api/companies');
        const companies = await response.json();
        const filter = document.getElementById('companyFilter');
        
        filter.innerHTML = '<option value="">All Companies</option>';

        companies.sort((a, b) => a.name.localeCompare(b.name));
        companies.forEach((company, index) => {
            const option = document.createElement("option");
            option.value = company.hash;
            option.textContent = company.name;
            filter.appendChild(option);
      
            if (index === 0) {
              option.selected = true;
            }
          });
    } catch (error) {
        console.error('Error loading companies:', error);
    }
}

function populateDepartments() {
    const departments = ['executive_leadership','operations','finance_accounting','human_resources',
        'legal_compliance','marketing_sales','customer_service_support','technology_it','product_rd',
        'supply_chain_logistics','other'];
    const filter = document.getElementById('department');
    departments.forEach(dept => {
        const option = document.createElement('option');
        option.value = dept;
        option.textContent = dept.split('_').map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
        filter.appendChild(option);
    });
}

document.addEventListener('DOMContentLoaded', populateDepartments);

document.addEventListener('DOMContentLoaded', populateCompanies);

document.getElementById('addCompanyBtn').addEventListener('click', () => {
    window.location.href = '/companies/add';
});

document.getElementById('salaryForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        company_hash: document.getElementById('companyFilter').value,
        years_at_the_company: parseInt(document.getElementById('years_at_the_company').value),
        total_experience: parseInt(document.getElementById('total_experience').value),
        salary_amount: parseFloat(document.getElementById('salary_amount').value),
        gender: document.getElementById('gender').value,
        submission_date: new Date().toISOString().split('T')[0],
        is_well_compensated: document.getElementById('is_well_compensated').value === "true",
        department: document.getElementById('department').value,
        job_title: document.getElementById('job_title').value
    };

    try {
        const response = await fetch('/api/salaries/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        const messageDiv = document.getElementById('message');

        if (response.ok) {
            messageDiv.style.display = 'block';
            messageDiv.style.backgroundColor = '#d4edda';
            messageDiv.style.color = '#155724';
            messageDiv.textContent = 'Submission successful! Thank you for your contribution.';
            document.getElementById('salaryForm').reset();

            setTimeout(() => {
                window.location.href = '/graph/employee';
            }, 500);
        } else {
            messageDiv.style.display = 'block';
            messageDiv.style.backgroundColor = '#f8d7da';
            messageDiv.style.color = '#721c24';
            messageDiv.textContent = result.error || 'Error submitting salary data';
        }

        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);

    } catch (error) {
        console.error('Error:', error);
        const messageDiv = document.getElementById('message');
        messageDiv.style.display = 'block';
        messageDiv.style.backgroundColor = '#f8d7da';
        messageDiv.style.color = '#721c24';
        messageDiv.textContent = 'Network error - please try again later.';
    }
});