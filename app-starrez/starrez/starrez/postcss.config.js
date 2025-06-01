const isProd = process.env.NODE_ENV === 'production';

module.exports = {
  plugins: {
    // Import resolver
    'postcss-import': {},
    
    // Tailwind CSS
    tailwindcss: {},
    
    // Autoprefixer for browser compatibility
    autoprefixer: {},
    
    // Production optimizations
    ...(isProd && {
      // Minify CSS in production
      cssnano: {
        preset: [
          'default',
          {
            discardComments: {
              removeAll: true,
            },
            // Preserve calc() functions for Tailwind
            calc: false,
            // Preserve CSS custom properties
            reduceIdents: false,
            // Don't merge longhand properties
            mergeLonghand: false,
          },
        ],
      },
      
      // Remove unused CSS (PurgeCSS)
      '@fullhuman/postcss-purgecss': {
        content: [
          './src/**/*.html',
          './src/**/*.js',
          './templates/**/*.html',
          './templates/**/*.yaml',
        ],
        defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
        safelist: {
          // Preserve these classes even if not found in content
          standard: [
            'active',
            'hidden',
            'opacity-75',
            'bg-gray-50',
            'line-through',
            'text-gray-500',
            'animate-bounce',
            /^bg-.*-\d+$/,
            /^text-.*-\d+$/,
            /^border-.*-\d+$/,
            /^hover:/,
            /^focus:/,
            /^transition-/,
          ],
          // Preserve classes with dynamic content
          deep: [
            /filter-btn/,
            /checklist-/,
            /timeline-/,
            /modal-/,
            /college-/,
            /flower-/,
          ],
          // Preserve keyframe animations
          greedy: [
            /animate-/,
            /transition-/,
            /duration-/,
            /ease-/,
          ],
        },
        // Skip files that should not be purged
        rejected: true,
        printRejected: false,
      },
    }),
  },
}