let barChart = null;
let pieChart = null;

$(document).ready(async function() {
    $('#companyFilter').select2({
        placeholder: "Search company...",
        allowClear: true,
        minimumResultsForSearch: -1
    });

    await populateCompanies();
    populateDepartments();
    populateExperienceLevels();
    fetchData();

    $('#applyFilters').click(fetchData);
});

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
        $('#companyFilter').trigger('change.select2');
    } catch (error) {
        console.error('Error loading companies:', error);
    }
}

function populateDepartments() {
    const departments = ['executive_leadership','operations','finance_accounting','human_resources',
        'legal_compliance','marketing_sales','customer_service_support','technology_it','product_rd',
        'supply_chain_logistics','other'];
    const filter = document.getElementById('departmentFilter');
    departments.forEach(dept => {
        const option = document.createElement('option');
        option.value = dept;
        option.textContent = dept.split('_').map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
        filter.appendChild(option);
    });
}

function populateExperienceLevels() {
    const levels = ['entry_level','junior','mid_level','senior','expert','legendary'];
    const filter = document.getElementById('experienceLevelFilter');
    levels.forEach(level => {
        const option = document.createElement('option');
        option.value = level;
        option.textContent = level.split('_').map(word => word[0].toUpperCase() + word.slice(1)).join(' ');
        filter.appendChild(option);
    });
}

async function fetchData() {
    try {
        const filters = {
            company_hash: $('#companyFilter').val(),
            department: $('#departmentFilter').val(),
            experience_level: $('#experienceLevelFilter').val(),
            gender: $('#genderFilter').val(),
            range_steps: $('#rangeStepFilter').val()
        };

        const filteredParams = Object.fromEntries(
            Object.entries(filters).filter(([_, value]) => value !== '')
        );

        const params = new URLSearchParams(filteredParams);
        const parameter = params.toString() ? `?${params.toString()}` : '';

        const response = await fetch(`/api/graphs/employee${parameter}`);
        const data = await response.json();
        updateCharts(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateCharts(data) {
    if (barChart) barChart.destroy();
    if (pieChart) pieChart.destroy();

    const barData = data.bar_graph;
    const currentValue = data.current;
    const labels = barData.map(b => b.range_start.toString());
    const counts = barData.map(b => b.count);
    let highlightIndex = barData.findIndex(b => currentValue >= b.range_start);
    if (highlightIndex === -1) highlightIndex = barData.length - 1;

    const barCtx = document.getElementById('barChart').getContext('2d');
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: counts,
                backgroundColor: counts.map((_, index) => index === highlightIndex ? 'rgba(255, 99, 132, 0.8)' : 'rgba(54, 162, 235, 0.8)'),
                borderColor: 'rgba(75, 75, 75, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'Count' } },
                x: { title: { display: true, text: 'Range Start' }, ticks: { autoSkip: false, maxRotation: 90, minRotation: 90 } }
            }
        }
    });

    const pieData = data.pie_graph;
    const compensated = pieData.find(p => p.is_well_compensated === 1)?.count || 0;
    const notCompensated = pieData.find(p => p.is_well_compensated === 0)?.count || 0;

    const pieCtx = document.getElementById('pieChart').getContext('2d');
    pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: ['Well Compensated', 'Not Well Compensated'],
            datasets: [{
                data: [compensated, notCompensated],
                backgroundColor: ['rgba(75, 192, 192, 0.8)', 'rgba(255, 99, 132, 0.8)'],
                borderColor: 'rgba(75, 75, 75, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: 'Compensation Distribution' }
            }
        }
    });
}