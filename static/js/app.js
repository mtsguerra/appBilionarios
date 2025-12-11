// API Base URL
const API_BASE = '/api';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadStatistics();
    loadBillionaires();
    loadCountries();
    loadIndustries();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('searchBtn').addEventListener('click', performSearch);
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    document.getElementById('applyFilters').addEventListener('click', applyFilters);
    document.getElementById('clearFilters').addEventListener('click', clearFilters);
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        displayStatistics(data);
    } catch (error) {
        console.error('Error loading statistics:', error);
        document.getElementById('statsContainer').innerHTML = '<p class="error">Error loading statistics</p>';
    }
}

// Display statistics
function displayStatistics(data) {
    const container = document.getElementById('statsContainer');
    const overall = data.overall;
    
    container.innerHTML = `
        <div class="stat-card">
            <h3>${overall.totalBillionaires}</h3>
            <p>Total Billionaires</p>
        </div>
        <div class="stat-card">
            <h3>$${(overall.avgWorth / 1000).toFixed(1)}B</h3>
            <p>Average Worth</p>
        </div>
        <div class="stat-card">
            <h3>$${(overall.maxWorth / 1000).toFixed(1)}B</h3>
            <p>Highest Worth</p>
        </div>
        <div class="stat-card">
            <h3>$${(overall.totalWorth / 1000).toFixed(1)}B</h3>
            <p>Total Worth</p>
        </div>
        <div class="stat-card">
            <h3>${data.ageStatistics.avgAge.toFixed(1)}</h3>
            <p>Average Age</p>
        </div>
        <div class="stat-card">
            <h3>${data.genderDistribution.find(g => g.gender === 'M')?.count || 0}M / ${data.genderDistribution.find(g => g.gender === 'F')?.count || 0}F</h3>
            <p>Gender Distribution</p>
        </div>
    `;
}

// Load billionaires
async function loadBillionaires(filters = {}) {
    const container = document.getElementById('billionairesList');
    container.innerHTML = '<p class="loading">Loading billionaires...</p>';
    
    try {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE}/billionaires?${params}`);
        const billionaires = await response.json();
        displayBillionaires(billionaires);
    } catch (error) {
        console.error('Error loading billionaires:', error);
        container.innerHTML = '<p class="error">Error loading billionaires</p>';
    }
}

// Display billionaires
function displayBillionaires(billionaires) {
    const container = document.getElementById('billionairesList');
    
    if (billionaires.length === 0) {
        container.innerHTML = '<p>No billionaires found</p>';
        return;
    }
    
    container.innerHTML = billionaires.map(b => `
        <div class="billionaire-card" onclick="viewBillionaire(${b.rank})">
            <span class="rank">Rank #${b.rank}</span>
            <h3>${b.personName}</h3>
            <div class="worth">$${(b.finalWorth / 1000).toFixed(1)} Billion</div>
            <div class="info">
                <strong>Title:</strong> ${b.title || 'N/A'}<br>
                <strong>Company:</strong> ${b.organization || 'N/A'}<br>
                <strong>Industry:</strong> ${b.category || 'N/A'}<br>
                <strong>Age:</strong> ${b.age || 'N/A'} | 
                <strong>Gender:</strong> ${b.gender || 'N/A'}<br>
                <strong>Country:</strong> ${b.countryOfCitizenship || 'N/A'}<br>
                <strong>City:</strong> ${b.cityName || 'N/A'}<br>
                <strong>Self-Made:</strong> ${b.selfMade ? 'Yes' : 'No'}
            </div>
        </div>
    `).join('');
}

// View billionaire details
async function viewBillionaire(rank) {
    try {
        const response = await fetch(`${API_BASE}/billionaire/${rank}`);
        const billionaire = await response.json();
        
        if (billionaire.error) {
            alert('Billionaire not found');
            return;
        }
        
        // Display detailed information in an alert (could be a modal in production)
        alert(`
Detailed Information for ${billionaire.personName}

Rank: #${billionaire.rank}
Full Name: ${billionaire.firstName} ${billionaire.lastName}
Net Worth: $${(billionaire.finalWorth / 1000).toFixed(1)} Billion
Age: ${billionaire.age} years old
Gender: ${billionaire.gender}
Birth Date: ${billionaire.birthDate}

Company: ${billionaire.organization}
Industry: ${billionaire.category}
Industries: ${billionaire.industries}
Title: ${billionaire.title}

Location: ${billionaire.cityName}, ${billionaire.state}
Country: ${billionaire.countryOfCitizenship}

Country Statistics:
- Population: ${billionaire.population?.toLocaleString() || 'N/A'}
- GDP: $${billionaire.gdp ? (billionaire.gdp / 1000000000000).toFixed(2) + 'T' : 'N/A'}
- Life Expectancy: ${billionaire.lifeExpectancy || 'N/A'} years
- CPI: ${billionaire.cpi || 'N/A'}
        `);
    } catch (error) {
        console.error('Error loading billionaire details:', error);
        alert('Error loading details');
    }
}

// Load countries
async function loadCountries() {
    const container = document.getElementById('countriesList');
    container.innerHTML = '<p class="loading">Loading countries...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/countries`);
        const countries = await response.json();
        displayCountries(countries);
        populateCountryFilter(countries);
    } catch (error) {
        console.error('Error loading countries:', error);
        container.innerHTML = '<p class="error">Error loading countries</p>';
    }
}

// Display countries
function displayCountries(countries) {
    const container = document.getElementById('countriesList');
    
    if (countries.length === 0) {
        container.innerHTML = '<p>No countries found</p>';
        return;
    }
    
    container.innerHTML = countries.map(c => `
        <div class="country-card">
            <h3>${c.countryName}</h3>
            <div class="info">
                <strong>Billionaires:</strong> ${c.billionaireCount}<br>
                <strong>Average Worth:</strong> $${(c.avgWorth / 1000).toFixed(1)}B<br>
                <strong>Total Worth:</strong> $${(c.totalWorth / 1000).toFixed(1)}B<br>
                <strong>Population:</strong> ${c.population?.toLocaleString() || 'N/A'}<br>
                <strong>GDP:</strong> ${c.gdp ? '$' + (c.gdp / 1000000000000).toFixed(2) + 'T' : 'N/A'}<br>
                <strong>Life Expectancy:</strong> ${c.lifeExpectancy || 'N/A'} years
            </div>
        </div>
    `).join('');
}

// Populate country filter
function populateCountryFilter(countries) {
    const select = document.getElementById('countryFilter');
    countries.forEach(c => {
        const option = document.createElement('option');
        option.value = c.countryName;
        option.textContent = `${c.countryName} (${c.billionaireCount})`;
        select.appendChild(option);
    });
}

// Load industries
async function loadIndustries() {
    const container = document.getElementById('industriesList');
    container.innerHTML = '<p class="loading">Loading industries...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/industries`);
        const industries = await response.json();
        displayIndustries(industries);
    } catch (error) {
        console.error('Error loading industries:', error);
        container.innerHTML = '<p class="error">Error loading industries</p>';
    }
}

// Display industries
function displayIndustries(industries) {
    const container = document.getElementById('industriesList');
    
    if (industries.length === 0) {
        container.innerHTML = '<p>No industries found</p>';
        return;
    }
    
    container.innerHTML = industries.map(i => `
        <div class="industry-card">
            <h3>${i.category}</h3>
            <div class="info">
                <strong>Industries:</strong> ${i.industries}<br>
                <strong>Billionaires:</strong> ${i.billionaireCount}<br>
                <strong>Average Worth:</strong> $${(i.avgWorth / 1000).toFixed(1)}B<br>
                <strong>Total Worth:</strong> $${(i.totalWorth / 1000).toFixed(1)}B
            </div>
        </div>
    `).join('');
}

// Perform search
async function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    const resultsContainer = document.getElementById('searchResults');
    
    if (!query) {
        resultsContainer.innerHTML = '';
        return;
    }
    
    resultsContainer.innerHTML = '<p class="loading">Searching...</p>';
    
    try {
        const response = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
        const results = await response.json();
        
        if (results.error) {
            resultsContainer.innerHTML = `<p class="error">${results.error}</p>`;
            return;
        }
        
        if (results.length === 0) {
            resultsContainer.innerHTML = '<p>No results found</p>';
            return;
        }
        
        resultsContainer.innerHTML = results.map(r => `
            <div class="search-result-card" onclick="viewBillionaire(${r.rank})">
                <h3>${r.personName} (Rank #${r.rank})</h3>
                <div class="info">
                    <strong>Worth:</strong> $${(r.finalWorth / 1000).toFixed(1)}B | 
                    <strong>Age:</strong> ${r.age || 'N/A'}<br>
                    <strong>Company:</strong> ${r.organization || 'N/A'} | 
                    <strong>Category:</strong> ${r.category || 'N/A'}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error performing search:', error);
        resultsContainer.innerHTML = '<p class="error">Error performing search</p>';
    }
}

// Apply filters
function applyFilters() {
    const filters = {};
    
    const country = document.getElementById('countryFilter').value;
    const gender = document.getElementById('genderFilter').value;
    const selfMade = document.getElementById('selfMadeFilter').value;
    
    if (country) filters.country = country;
    if (gender) filters.gender = gender;
    if (selfMade) filters.selfMade = selfMade;
    
    loadBillionaires(filters);
}

// Clear filters
function clearFilters() {
    document.getElementById('countryFilter').value = '';
    document.getElementById('genderFilter').value = '';
    document.getElementById('selfMadeFilter').value = '';
    loadBillionaires();
}
