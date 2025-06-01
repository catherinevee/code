// Universal Search Component for College Website
class SearchComponent {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            placeholder: options.placeholder || 'Search...',
            minChars: options.minChars || 2,
            debounceMs: options.debounceMs || 300,
            categories: options.categories || [],
            onSearch: options.onSearch || (() => {}),
            onFilter: options.onFilter || (() => {}),
            showFilters: options.showFilters !== false
        };
        
        this.searchTimeout = null;
        this.currentQuery = '';
        this.activeFilters = new Set();
        
        this.init();
    }
    
    init() {
        this.render();
        this.attachEventListeners();
    }
    
    render() {
        const searchHTML = `
            <div class="search-component bg-white rounded-lg shadow-lg p-6 mb-8">
                <!-- Search Input -->
                <div class="relative mb-4">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                    </div>
                    <input type="text" 
                           class="search-input block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-college-blue focus:border-college-blue" 
                           placeholder="${this.options.placeholder}">
                    <div class="search-clear absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer hidden">
                        <svg class="h-5 w-5 text-gray-400 hover:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </div>
                </div>
                
                <!-- Filters -->
                ${this.options.showFilters ? this.renderFilters() : ''}
                
                <!-- Search Results Summary -->
                <div class="search-summary hidden">
                    <div class="flex items-center justify-between">
                        <span class="text-sm text-gray-600">
                            <span class="results-count">0</span> results found
                            <span class="search-query-display"></span>
                        </span>
                        <button class="clear-search text-sm text-college-blue hover:text-college-gold">
                            Clear search
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        this.container.innerHTML = searchHTML;
    }
    
    renderFilters() {
        if (!this.options.categories.length) return '';
        
        return `
            <div class="filters-section">
                <h4 class="text-sm font-medium text-gray-900 mb-3">Filter by:</h4>
                <div class="flex flex-wrap gap-2">
                    ${this.options.categories.map(category => `
                        <button class="filter-btn px-3 py-1 text-sm border border-gray-300 rounded-full hover:border-college-blue hover:text-college-blue transition-colors" 
                                data-filter="${category.value}">
                            ${category.label}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    attachEventListeners() {
        const searchInput = this.container.querySelector('.search-input');
        const searchClear = this.container.querySelector('.search-clear');
        const clearSearch = this.container.querySelector('.clear-search');
        const filterBtns = this.container.querySelectorAll('.filter-btn');
        
        // Search input with debouncing
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            this.currentQuery = query;
            
            // Show/hide clear button
            if (query) {
                searchClear.classList.remove('hidden');
            } else {
                searchClear.classList.add('hidden');
            }
            
            // Debounced search
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                this.performSearch(query);
            }, this.options.debounceMs);
        });
        
        // Clear search button
        if (searchClear) {
            searchClear.addEventListener('click', () => {
                searchInput.value = '';
                this.currentQuery = '';
                searchClear.classList.add('hidden');
                this.clearSearch();
            });
        }
        
        // Clear search link
        if (clearSearch) {
            clearSearch.addEventListener('click', () => {
                searchInput.value = '';
                this.currentQuery = '';
                searchClear.classList.add('hidden');
                this.activeFilters.clear();
                this.updateFilterButtons();
                this.clearSearch();
            });
        }
        
        // Filter buttons
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.dataset.filter;
                this.toggleFilter(filter);
                this.updateFilterButtons();
                this.performSearch(this.currentQuery);
            });
        });
    }
    
    toggleFilter(filter) {
        if (this.activeFilters.has(filter)) {
            this.activeFilters.delete(filter);
        } else {
            this.activeFilters.add(filter);
        }
    }
    
    updateFilterButtons() {
        const filterBtns = this.container.querySelectorAll('.filter-btn');
        filterBtns.forEach(btn => {
            const filter = btn.dataset.filter;
            if (this.activeFilters.has(filter)) {
                btn.classList.add('bg-college-blue', 'text-white', 'border-college-blue');
                btn.classList.remove('border-gray-300', 'hover:border-college-blue', 'hover:text-college-blue');
            } else {
                btn.classList.remove('bg-college-blue', 'text-white', 'border-college-blue');
                btn.classList.add('border-gray-300', 'hover:border-college-blue', 'hover:text-college-blue');
            }
        });
    }
    
    performSearch(query) {
        const shouldSearch = query.length >= this.options.minChars || this.activeFilters.size > 0;
        
        if (shouldSearch) {
            this.options.onSearch(query, Array.from(this.activeFilters));
            this.showSearchSummary(query);
        } else if (query.length === 0 && this.activeFilters.size === 0) {
            this.clearSearch();
        }
    }
    
    showSearchSummary(query) {
        const summary = this.container.querySelector('.search-summary');
        const queryDisplay = this.container.querySelector('.search-query-display');
        
        if (summary) {
            summary.classList.remove('hidden');
            if (query) {
                queryDisplay.textContent = ` for "${query}"`;
            } else {
                queryDisplay.textContent = '';
            }
        }
    }
    
    updateResultCount(count) {
        const resultCount = this.container.querySelector('.results-count');
        if (resultCount) {
            resultCount.textContent = count;
        }
    }
    
    clearSearch() {
        const summary = this.container.querySelector('.search-summary');
        if (summary) {
            summary.classList.add('hidden');
        }
        this.options.onSearch('', []);
    }
}

// Search utilities for different content types
class SearchUtilities {
    static searchDorms(dorms, query, filters) {
        let results = [...dorms];
        
        // Apply text search
        if (query) {
            const searchTerm = query.toLowerCase();
            results = results.filter(dorm => 
                dorm.name.toLowerCase().includes(searchTerm) ||
                dorm.description.toLowerCase().includes(searchTerm) ||
                dorm.flowerType.toLowerCase().includes(searchTerm) ||
                dorm.amenities.some(amenity => amenity.toLowerCase().includes(searchTerm))
            );
        }
        
        // Apply filters
        if (filters.length > 0) {
            results = results.filter(dorm => {
                return filters.some(filter => {
                    switch (filter) {
                        case 'single':
                            return dorm.roomTypes.includes('Single');
                        case 'double':
                            return dorm.roomTypes.includes('Double');
                        case 'suite':
                            return dorm.roomTypes.includes('Suite');
                        case 'small':
                            return dorm.capacity <= 100;
                        case 'medium':
                            return dorm.capacity > 100 && dorm.capacity <= 200;
                        case 'large':
                            return dorm.capacity > 200;
                        default:
                            return true;
                    }
                });
            });
        }
        
        return results;
    }
    
    static searchStudyAreas(studyAreas, query, filters) {
        let results = [...studyAreas];
        
        // Apply text search
        if (query) {
            const searchTerm = query.toLowerCase();
            results = results.filter(area => 
                area.name.toLowerCase().includes(searchTerm) ||
                area.description.toLowerCase().includes(searchTerm) ||
                area.type.toLowerCase().includes(searchTerm) ||
                area.location.toLowerCase().includes(searchTerm) ||
                area.amenities.some(amenity => amenity.toLowerCase().includes(searchTerm))
            );
        }
        
        // Apply filters
        if (filters.length > 0) {
            results = results.filter(area => {
                return filters.some(filter => {
                    switch (filter) {
                        case 'quiet':
                            return area.noise_level === 'Quiet';
                        case 'moderate':
                            return area.noise_level === 'Moderate';
                        case 'collaborative':
                            return area.noise_level === 'Collaborative';
                        case 'library':
                            return area.type === 'Library';
                        case 'center':
                            return area.type === 'Student Center';
                        case 'outdoor':
                            return area.type === 'Outdoor Study';
                        case 'reservation':
                            return area.reservation_required;
                        case 'no-reservation':
                            return !area.reservation_required;
                        default:
                            return true;
                    }
                });
            });
        }
        
        return results;
    }
    
    static highlightMatches(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark class="bg-yellow-200">$1</mark>');
    }
}