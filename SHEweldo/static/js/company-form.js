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
		option.textContent =
			industry.charAt(0).toUpperCase() + industry.slice(1);
		filter.appendChild(option);
	});
}

document.getElementById("companyForm").addEventListener("submit", async (e) => {
	e.preventDefault();

	const companyName = document.getElementById("company_name").value.trim();
	const companySize = parseInt(document.getElementById("company_size").value);
	const industry = document.getElementById("industry").value;
	const country = document.getElementById("country").value.trim();

	const messageDiv = document.getElementById("message");

	if (!companyName || companyName.length < 2 || companyName.length > 100) {
		messageDiv.style.display = "block";
		messageDiv.style.backgroundColor = "#f8d7da";
		messageDiv.style.color = "#721c24";
		messageDiv.textContent =
			"Company name must be between 2 and 100 characters.";
		return;
	}

	if (isNaN(companySize) || companySize < 1 || companySize > 1000000) {
		messageDiv.style.display = "block";
		messageDiv.style.backgroundColor = "#f8d7da";
		messageDiv.style.color = "#721c24";
		messageDiv.textContent =
			"Company size must be a number between 1 and 1,000,000.";
		return;
	}

	if (!industry) {
		messageDiv.style.display = "block";
		messageDiv.style.backgroundColor = "#f8d7da";
		messageDiv.style.color = "#721c24";
		messageDiv.textContent = "Please select an industry.";
		return;
	}

	if (!country || country.length < 2 || country.length > 100) {
		messageDiv.style.display = "block";
		messageDiv.style.backgroundColor = "#f8d7da";
		messageDiv.style.color = "#721c24";
		messageDiv.textContent =
			"Country must be between 2 and 100 characters.";
		return;
	}

	const formData = {
		company_name: companyName,
		company_size: companySize,
		company_industry: industry,
		country: country,
	};

	try {
		const response = await fetch("/api/company/submit", {
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
			messageDiv.textContent = "Company added successfully!";
			document.getElementById("companyForm").reset();

			setTimeout(() => {
				window.open("/employee/submit", "_blank");
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
		messageDiv.style.display = "block";
		messageDiv.style.backgroundColor = "#f8d7da";
		messageDiv.style.color = "#721c24";
		messageDiv.textContent = "Network error - please try again later.";
	}
});