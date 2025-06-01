class ContentLoader {
    constructor() {
        this.cache = new Map();
    }
    
    async loadJSON(url) {
        if (this.cache.has(url)) {
            return this.cache.get(url);
        }
        
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this.cache.set(url, data);
            return data;
        } catch (error) {
            console.error('Error loading content:', error);
            return null;
        }
    }
    
    async loadDorms() {
        return await this.loadJSON('/data/dorms.json');
    }
    
    async loadStudyAreas() {
        return await this.loadJSON('/data/study-areas.json');
    }
    
    async loadSiteConfig() {
        return await this.loadJSON('/data/site-config.json');
    }
}

// Initialize content loader
const contentLoader = new ContentLoader();

// DOM utility functions
function createElement(tag, className, content) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (content) element.innerHTML = content;
    return element;
}

function renderDormCard(dorm) {
    return `
        <div class="bg-white overflow-hidden shadow rounded-lg">
            <img class="h-48 w-full object-cover" src="${dorm.image}" alt="${dorm.name}">
            <div class="p-6">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <div class="h-10 w-10 bg-flower-pink rounded-full flex items-center justify-center">
                            <span class="text-white font-semibold">${dorm.flowerType[0]}</span>
                        </div>
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-medium text-gray-900">${dorm.name}</h3>
                        <p class="text-sm text-gray-500">Capacity: ${dorm.capacity} students</p>
                    </div>
                </div>
                <p class="mt-4 text-gray-600">${dorm.description}</p>
                
                <div class="mt-4">
                    <h4 class="text-sm font-medium text-gray-900">Amenities:</h4>
                    <ul class="mt-2 text-sm text-gray-600">
                        ${dorm.amenities.map(amenity => `
                            <li class="flex items-center">
                                <svg class="h-4 w-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                                </svg>
                                ${amenity}
                            </li>
                        `).join('')}
                    </ul>
                </div>
                
                <div class="mt-6 flex justify-between items-center">
                    <div class="text-sm text-gray-500">
                        <p>📞 ${dorm.contact.phone}</p>
                        <p>✉️ ${dorm.contact.email}</p>
                    </div>
                    <button class="bg-college-blue text-white px-4 py-2 rounded hover:bg-blue-700">
                        Learn More
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Page-specific initialization
document.addEventListener('DOMContentLoaded', async function() {
    const currentPage = window.location.pathname.split('/').pop();
    
    switch(currentPage) {
        case 'dorms.html':
            await initializeDormsPage();
            break;
        case 'study-areas.html':
            await initializeStudyAreasPage();
            break;
        default:
            console.log('No specific initialization needed for this page');
    }
});

async function initializeDormsPage() {
    const dormsData = await contentLoader.loadDorms();
    if (dormsData && dormsData.dorms) {
        const container = document.getElementById('dorms-container');
        if (container) {
            container.innerHTML = dormsData.dorms.map(renderDormCard).join('');
        }
    }
}

async function initializeStudyAreasPage() {
    const studyAreasData = await contentLoader.loadStudyAreas();
    if (studyAreasData && studyAreasData.studyAreas) {
        const container = document.getElementById('study-areas-container');
        if (container) {
            container.innerHTML = studyAreasData.studyAreas.map(renderStudyAreaCard).join('');
        }
    }
}