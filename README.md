# Vardan Barsegyan — academic website

Source for [www.vardanbarsegyan.com](https://www.vardanbarsegyan.com), a Jekyll-based academic website maintained in the `vardanbarsegyan/vardanbarsegyan.github.io` repository.

## Local development

The supported toolchain is Ruby 3.3.12 and Node.js 24 LTS. Version files are included for Ruby and Node version managers.

```bash
bundle install
npm install
bundle exec jekyll serve --livereload
```

Open `http://127.0.0.1:4000`. Build and check the production output with:

```bash
bundle exec jekyll build --strict_front_matter
bundle exec htmlproofer ./_site --disable-external
```

## Content and assets

- Site-wide identity, profiles, analytics, and collection settings: `_config.yml`
- Main navigation: `_data/navigation.yml`
- Main pages: `_pages/`
- Curated resource lists: `resources/`
- CV, worksheets, and other downloads: `files/`
- PVI presentations and interactive maps: `_publications/`
- Images and social preview: `images/`

The theme CSS is stored as compiled static files in `assets/css/`. JavaScript sources remain in `assets/js/`; after changing them, run `npm run build:js` and commit the regenerated `assets/js/main.min.js`.

The Political Voice Inequality maps share the locally hosted `assets/js/plotly-geo-3.6.0.min.js` bundle. This avoids an external runtime dependency and keeps the map pages much smaller than their former standalone exports.

## Deployment

The GitHub Actions workflow builds, checks, and deploys the site to GitHub Pages after changes reach the `master` branch. The custom domain is defined in `CNAME`. Configure the repository’s Pages source as **GitHub Actions** before the first workflow deployment.

## Privacy

Google Analytics 4 is enabled through `_config.yml`. The Impact page links to a Google Form; submissions and Google’s handling of form data occur on Google’s service. The public privacy notice is in `_pages/terms.md`.

## Credits and license

The presentation layer is based on the [Academic Pages](https://github.com/academicpages/academicpages.github.io) theme, itself derived from Minimal Mistakes. See `LICENSE` for the inherited MIT license.
