/**
 * ==========================================================================
 * MUTENROS Portfolio - GitHub Projects Module
 * ==========================================================================
 * 
 * Handles GitHub API integration:
 * - Fetching public repositories
 * - Combining with private project data
 * - Rendering project cards
 * 
 * @author Dario (MutenRos)
 * @version 2.0.0
 * @license MIT
 * ==========================================================================
 */

import CONFIG from '../config.js';
import { escapeHtml } from './utils.js';

/**
 * GitHubProjects Class
 * Manages GitHub repository fetching and project display
 */
class GitHubProjects {
    /**
     * Initialize GitHub projects handler
     * @param {Object} options - Configuration options
     */
    constructor(options = {}) {
        this.container = null;
        this.options = {
            username: options.username || CONFIG.github.username,
            perPage: options.perPage || CONFIG.github.reposPerPage,
            sortBy: options.sortBy || CONFIG.github.sortBy,
            excludeRepos: options.excludeRepos || CONFIG.github.excludeRepos,
            excludeForks: options.excludeForks !== false
        };
        
        this.isLoading = false;
        this.projects = [];
    }
    
    /**
     * Initialize and load projects
     * @param {string|Element} containerSelector - Container for project cards
     */
    async init(containerSelector = '#projects-grid') {
        this.container = typeof containerSelector === 'string'
            ? document.querySelector(containerSelector)
            : containerSelector;
        
        if (!this.container) {
            console.error('[GitHubProjects] Container not found:', containerSelector);
            return;
        }
        
        await this.loadProjects();
        console.log('[GitHubProjects] Initialized');
    }
    
    /**
     * Load and display all projects
     */
    async loadProjects() {
        if (this.isLoading) return;
        this.isLoading = true;
        
        this.showLoading();
        
        try {
            // Fetch public repos from GitHub API
            const publicRepos = await this.fetchGitHubRepos();
            
            // Combine with private projects
            this.projects = this.combineProjects(publicRepos);
            
            // Render project cards
            this.renderProjects();
            
        } catch (error) {
            console.error('[GitHubProjects] Error loading projects:', error);
            this.showError();
        } finally {
            this.isLoading = false;
        }
    }
    
    /**
     * Fetch repositories from GitHub API
     * @returns {Promise<Array>} Array of repository objects
     */
    async fetchGitHubRepos() {
        const url = `${CONFIG.github.apiBaseUrl}/users/${this.options.username}/repos` +
                    `?sort=${this.options.sortBy}&per_page=${this.options.perPage}`;
        
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`GitHub API error: ${response.status}`);
        }
        
        const repos = await response.json();
        
        // Filter out excluded repos and forks
        return repos.filter(repo => {
            // Exclude specified repos
            if (this.options.excludeRepos.includes(repo.name)) {
                return false;
            }
            // Exclude forks if configured
            if (this.options.excludeForks && repo.fork) {
                return false;
            }
            return true;
        });
    }
    
    /**
     * Combine public repos with private projects
     * @param {Array} publicRepos - Repos from GitHub API
     * @returns {Array} Combined projects array
     */
    combineProjects(publicRepos) {
        // Map private projects
        const privateProjects = CONFIG.privateProjects.map(project => ({
            ...project,
            isPrivate: true
        }));
        
        // Map public repos
        const publicProjects = publicRepos.map(repo => ({
            name: repo.name,
            description: repo.description,
            language: repo.language,
            homepage: repo.homepage,
            html_url: repo.html_url,
            has_pages: repo.has_pages,
            stargazers_count: repo.stargazers_count,
            forks_count: repo.forks_count,
            topics: repo.topics,
            isPrivate: false
        }));
        
        // Private projects first, then public
        return [...privateProjects, ...publicProjects];
    }
    
    /**
     * Render all project cards
     */
    renderProjects() {
        if (this.projects.length === 0) {
            this.showEmpty();
            return;
        }
        
        const html = this.projects.map(project => 
            project.isPrivate 
                ? this.renderPrivateProjectCard(project)
                : this.renderPublicProjectCard(project)
        ).join('');
        
        this.container.innerHTML = html;
    }
    
    /**
     * Render a private project card
     * @param {Object} project - Project data
     * @returns {string} HTML string
     */
    renderPrivateProjectCard(project) {
        const iconHtml = project.icon 
            ? `<i class="${project.icon}"></i>` 
            : '<i class="fa-solid fa-lock"></i>';
        
        const languageTag = project.language 
            ? `<span class="project-card__tag">${escapeHtml(project.language.toUpperCase())}</span>` 
            : '';
        
        const demoLink = project.homepage 
            ? `<a href="${escapeHtml(project.homepage)}" target="_blank" rel="noopener noreferrer" class="project-card__link project-card__link--demo">VER DEMO</a>` 
            : '';
        
        return `
            <article class="project-card">
                <div class="project-card__image">
                    <span class="project-card__image--icon">${iconHtml}</span>
                </div>
                <div class="project-card__info">
                    <h3 class="project-card__title">
                        ${escapeHtml(project.name)}
                        <span class="project-card__badge">
                            <i class="fa-solid fa-lock"></i> PRIVATE
                        </span>
                    </h3>
                    <p class="project-card__description">
                        ${escapeHtml(project.description || 'Proyecto con codigo privado.')}
                    </p>
                    <div class="project-card__tags">
                        ${languageTag}
                    </div>
                    <div class="project-card__links">
                        ${demoLink}
                    </div>
                </div>
            </article>
        `;
    }
    
    /**
     * Render a public project card
     * @param {Object} project - Project data
     * @returns {string} HTML string
     */
    renderPublicProjectCard(project) {
        const iconClass = this.getLanguageIcon(project.language);
        
        const languageTag = project.language 
            ? `<span class="project-card__tag">${escapeHtml(project.language.toUpperCase())}</span>` 
            : '';
        
        const topicsTags = (project.topics || [])
            .slice(0, 2)
            .map(topic => `<span class="project-card__tag">${escapeHtml(topic.toUpperCase())}</span>`)
            .join('');
        
        const hasDemo = project.has_pages || project.homepage;
        const demoUrl = project.homepage || `https://mutenros.github.io/${project.name}`;
        
        const demoLink = hasDemo 
            ? `<a href="${escapeHtml(demoUrl)}" target="_blank" rel="noopener noreferrer" class="project-card__link project-card__link--demo">DEMO</a>` 
            : '';
        
        return `
            <article class="project-card">
                <div class="project-card__image">
                    <span class="project-card__image--icon">
                        <i class="${iconClass}"></i>
                    </span>
                </div>
                <div class="project-card__info">
                    <h3 class="project-card__title">${escapeHtml(project.name)}</h3>
                    <p class="project-card__description">
                        ${escapeHtml(project.description || 'Sin descripcion disponible.')}
                    </p>
                    <div class="project-card__tags">
                        ${languageTag}
                        ${topicsTags}
                    </div>
                    <div class="project-card__stats">
                        <span class="project-card__stat">
                            <i class="fa-solid fa-star"></i> ${project.stargazers_count || 0}
                        </span>
                        <span class="project-card__stat">
                            <i class="fa-solid fa-code-fork"></i> ${project.forks_count || 0}
                        </span>
                    </div>
                    <div class="project-card__links">
                        <a href="${escapeHtml(project.html_url)}" target="_blank" rel="noopener noreferrer" class="project-card__link" aria-label="Ver codigo de ${escapeHtml(project.name)}">VER CODIGO</a>
                        ${demoLink}
                    </div>
                </div>
            </article>
        `;
    }
    
    /**
     * Get Font Awesome icon class for a programming language
     * @param {string} language - Programming language name
     * @returns {string} Icon class
     */
    getLanguageIcon(language) {
        return CONFIG.languageIcons[language] || CONFIG.languageIcons.default;
    }
    
    /**
     * Show loading state
     */
    showLoading() {
        this.container.innerHTML = `
            <div class="loading-message">
                <div class="loader"></div>
                <p class="loading-message__text">Cargando proyectos...</p>
            </div>
        `;
    }
    
    /**
     * Show error state
     */
    showError() {
        this.container.innerHTML = `
            <div class="no-projects">
                <p>Error al cargar proyectos. Intenta mas tarde.</p>
            </div>
        `;
    }
    
    /**
     * Show empty state
     */
    showEmpty() {
        this.container.innerHTML = `
            <div class="no-projects">
                <p>No hay proyectos publicos disponibles.</p>
            </div>
        `;
    }
}

// Create singleton instance
const githubProjects = new GitHubProjects();

export default githubProjects;
export { GitHubProjects };
