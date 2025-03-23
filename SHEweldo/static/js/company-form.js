document.addEventListener("DOMContentLoaded", function () {
	setTimeout(() => {
		document.querySelector(".formCompany").classList.add("show");
    populateIndustries();
	}, 100);
});

function populateIndustries() {
	const industries = [
	  "technology",
		"finance",
		"healthcare",
		"manufacturing",
		"retail",
		"education",
		"transportation",
		"energy",
		"entertainment",
		"telecommunications",
		"construction",
		"hospitality",
		"real estate",
		"agriculture",
		"pharmaceuticals",
		"other",
	];
	const filter = document.getElementById("industry");
	industries.forEach((industry) => {
	  const option = document.createElement("option");
	  option.value = industry;
	  option.textContent = industry.charAt(0).toUpperCase() + industry.slice(1);
	  filter.appendChild(option);
	});
  }

document.getElementById("companyForm").addEventListener("submit", async (e) => {
	e.preventDefault();

	const formData = {
		company_name: document.getElementById("company_name").value,
		company_size: parseInt(document.getElementById("company_size").value),
		company_industry: document.getElementById("company_industry").value,
		country: document.getElementById("country").value,
	};

	try {
		const response = await fetch("/api/companies/add", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(formData),
		});

		const result = await response.json();
		const messageDiv = document.getElementById("message");

		if (response.ok) {
			messageDiv.style.display = "block";
			messageDiv.style.backgroundColor = "#d4edda";
			messageDiv.style.color = "#155724";
			messageDiv.textContent = "Company added successfully!";
			document.getElementById("companyForm").reset();

			setTimeout(() => {
				window.open("/salaries/submit", "_blank");
			}, 1000);
		} else {
			messageDiv.style.display = "block";
			messageDiv.style.backgroundColor = "#f8d7da";
			messageDiv.style.color = "#721c24";
			messageDiv.textContent =
				result.error || "Error submitting company data";
		}

		setTimeout(() => {
			messageDiv.style.display = "none";
		}, 5000);
	} catch (error) {
		console.error("Error:", error);
		const messageDiv = document.getElementById("message");
		messageDiv.style.display = "block";
		messageDiv.style.backgroundColor = "#f8d7da";
		messageDiv.style.color = "#721c24";
		messageDiv.textContent = "Network error - please try again later.";
	}
});
