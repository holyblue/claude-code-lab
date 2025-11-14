# CLAUDE.md

**Repository Context File for AI Assistants**

This file provides essential context about the repository structure, development workflows, and conventions to help AI assistants like Claude Code work effectively with this codebase.

---

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Project Structure](#project-structure)
3. [Development Workflow](#development-workflow)
4. [Code Conventions](#code-conventions)
5. [Testing Strategy](#testing-strategy)
6. [Deployment Process](#deployment-process)
7. [Common Tasks](#common-tasks)
8. [AI Assistant Guidelines](#ai-assistant-guidelines)
9. [Troubleshooting](#troubleshooting)

---

## Repository Overview

### Purpose
This repository serves as a lab/example for working with Claude Code and documenting codebases for AI assistants.

### Tech Stack
- **Language**: [Primary programming language]
- **Framework**: [Main framework if applicable]
- **Build Tool**: [Build system]
- **Package Manager**: [npm, pip, cargo, etc.]
- **Testing**: [Testing framework]
- **CI/CD**: [GitHub Actions, etc.]

### Key Dependencies
List major dependencies and their purpose:
- `dependency-name`: Brief description of what it does

---

## Project Structure

```
/
├── .git/                 # Git repository metadata
├── src/                  # Source code
│   ├── components/       # Reusable components
│   ├── services/         # Business logic and API services
│   ├── utils/            # Utility functions and helpers
│   └── index.js          # Entry point
├── tests/                # Test files
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
├── docs/                 # Documentation
├── scripts/              # Build and utility scripts
├── config/               # Configuration files
├── package.json          # Project metadata and dependencies
├── .gitignore            # Git ignore rules
├── README.md             # User-facing documentation
└── CLAUDE.md             # This file - AI assistant context
```

### Key Directories

- **`src/`**: Contains all source code. Organized by feature/module.
- **`tests/`**: All test files mirror the structure of `src/`.
- **`docs/`**: Architecture decisions, API documentation, guides.
- **`scripts/`**: Automation scripts for common tasks.
- **`config/`**: Environment-specific configuration files.

---

## Development Workflow

### Branch Strategy

- **`main`**: Production-ready code. Protected branch.
- **`develop`**: Integration branch for features.
- **`feature/*`**: Feature branches (e.g., `feature/user-auth`)
- **`bugfix/*`**: Bug fix branches (e.g., `bugfix/login-error`)
- **`hotfix/*`**: Urgent production fixes
- **`claude/*`**: AI assistant working branches

### Branching Rules

1. Always create feature branches from `develop`
2. Branch names should be descriptive and kebab-case
3. Claude Code branches should start with `claude/` prefix
4. Delete branches after merging

### Commit Message Convention

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples:**
```
feat(auth): add OAuth2 authentication flow
fix(api): resolve null pointer exception in user service
docs(readme): update installation instructions
refactor(utils): simplify date formatting logic
```

### Pull Request Process

1. **Create PR** from your feature branch to target branch
2. **Fill PR template** with:
   - Summary of changes
   - Related issue numbers
   - Testing performed
   - Screenshots (if UI changes)
3. **Request review** from appropriate team members
4. **Address feedback** and update PR
5. **Merge** after approval (squash and merge preferred)

---

## Code Conventions

### General Principles

1. **DRY (Don't Repeat Yourself)**: Extract common logic
2. **KISS (Keep It Simple, Stupid)**: Favor simple solutions
3. **YAGNI (You Aren't Gonna Need It)**: Don't over-engineer
4. **Separation of Concerns**: Keep modules focused
5. **Self-Documenting Code**: Use clear names, add comments for complex logic

### Naming Conventions

- **Variables**: `camelCase` for local variables, `UPPER_SNAKE_CASE` for constants
- **Functions**: `camelCase`, verb-based (e.g., `getUserById`, `calculateTotal`)
- **Classes**: `PascalCase` (e.g., `UserService`, `DataProcessor`)
- **Files**: Match the main export, use kebab-case for utilities
- **Directories**: `kebab-case` or `camelCase` depending on ecosystem

### Code Style

- **Indentation**: 2 or 4 spaces (consistent across project)
- **Line Length**: Max 80-120 characters
- **Semicolons**: [Use them / Don't use them] - be consistent
- **Quotes**: Single or double quotes - be consistent
- **Trailing Commas**: Yes/No in multiline structures

### Documentation

- Add JSDoc/docstrings for public APIs
- Document complex algorithms with inline comments
- Keep comments up-to-date with code changes
- Prefer self-documenting code over excessive comments

### Error Handling

- Use try-catch blocks for async operations
- Create custom error classes for domain-specific errors
- Always log errors with context
- Never swallow exceptions silently

---

## Testing Strategy

### Test Structure

- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test interactions between modules
- **E2E Tests**: Test complete user workflows

### Running Tests

```bash
# Run all tests
npm test

# Run specific test suite
npm test -- path/to/test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

### Test Conventions

- Test file naming: `*.test.js` or `*.spec.js`
- One test file per source file
- Use descriptive test names: "should [expected behavior] when [condition]"
- Follow AAA pattern: Arrange, Act, Assert
- Mock external dependencies

### Coverage Goals

- Minimum 80% code coverage
- 100% coverage for critical business logic
- Focus on meaningful tests, not just coverage numbers

---

## Deployment Process

### Environment

- **Development**: Local development environment
- **Staging**: Pre-production testing environment
- **Production**: Live environment

### Deployment Steps

1. **Build**: `npm run build`
2. **Test**: `npm test`
3. **Lint**: `npm run lint`
4. **Deploy**: [Deployment command or CI/CD process]

### Environment Variables

Required environment variables:
- `NODE_ENV`: Environment (development/staging/production)
- `API_KEY`: API authentication key
- `DATABASE_URL`: Database connection string

Store sensitive values in:
- Local: `.env` file (gitignored)
- Production: Environment variables or secrets manager

---

## Common Tasks

### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd <repository-name>

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Run development server
npm run dev
```

### Adding a New Feature

1. Create feature branch: `git checkout -b feature/my-feature`
2. Implement feature with tests
3. Run tests: `npm test`
4. Run linter: `npm run lint`
5. Commit changes with conventional commit message
6. Push and create PR

### Updating Dependencies

```bash
# Check for outdated dependencies
npm outdated

# Update dependencies (carefully)
npm update

# Or update individual package
npm install package-name@latest

# Test thoroughly after updates
npm test
```

### Debugging

- Use built-in debugger: `debugger;` statement
- Console logging with context: `console.log('[ModuleName]', data)`
- Browser DevTools / Node debugger
- Check logs in: [log location]

---

## AI Assistant Guidelines

### Context Awareness

When working with this codebase, AI assistants should:

1. **Read this file first** to understand project structure and conventions
2. **Check existing patterns** before implementing new code
3. **Follow established conventions** for naming, structure, and style
4. **Maintain consistency** with existing codebase
5. **Ask for clarification** when requirements are ambiguous

### Best Practices for AI Assistants

#### Code Generation

- Match the existing code style exactly
- Use the same libraries and patterns already in the codebase
- Don't introduce new dependencies without good reason
- Follow the project's error handling patterns
- Write tests alongside implementation code

#### File Operations

- **Read before writing**: Always read existing files before modifying
- **Preserve formatting**: Maintain existing indentation and style
- **Incremental changes**: Make small, focused changes
- **Verify changes**: Double-check that edits match intent

#### Communication

- Explain what you're doing and why
- Highlight any assumptions you're making
- Warn about potential issues or trade-offs
- Provide file paths with line numbers for reference (e.g., `src/utils/helper.js:42`)

#### Git Workflow

- Create appropriately named branches (e.g., `claude/feature-name-<session-id>`)
- Write clear, conventional commit messages
- Commit logical chunks of work, not everything at once
- Push to the correct branch specified in instructions

### Common Patterns to Follow

#### Module Exports

```javascript
// Prefer named exports for better tree-shaking
export function myFunction() { }
export class MyClass { }

// Default export for main module functionality
export default MyModule;
```

#### Async/Await

```javascript
// Always use try-catch with async operations
async function fetchData() {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    logger.error('Failed to fetch data:', error);
    throw new CustomError('Data fetch failed', error);
  }
}
```

#### Configuration

```javascript
// Centralize configuration
const config = {
  api: {
    baseUrl: process.env.API_BASE_URL,
    timeout: 5000,
  },
  feature: {
    enabled: process.env.FEATURE_ENABLED === 'true',
  },
};
```

### Security Considerations

AI assistants must be vigilant about:

- **No hardcoded secrets**: Never commit API keys, passwords, or tokens
- **Input validation**: Always validate and sanitize user input
- **SQL injection**: Use parameterized queries, never string concatenation
- **XSS prevention**: Escape output, use framework protections
- **CSRF protection**: Implement CSRF tokens for state-changing operations
- **Dependency vulnerabilities**: Check for known vulnerabilities in dependencies

### Performance Considerations

- Avoid N+1 queries in database operations
- Use pagination for large datasets
- Implement caching where appropriate
- Optimize images and assets
- Lazy load non-critical resources
- Profile before optimizing (don't premature optimize)

---

## Troubleshooting

### Common Issues

#### Build Fails

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version matches requirements
node --version
```

#### Tests Failing

- Ensure test database is properly seeded
- Check for environment-specific issues
- Run tests in isolation to identify flaky tests
- Clear test cache if applicable

#### Import Errors

- Verify file paths are correct
- Check for circular dependencies
- Ensure exports/imports match
- Look for typos in module names

### Getting Help

- **Documentation**: Check `/docs` directory
- **Issues**: Search existing GitHub issues
- **Team**: Contact [team channel/email]
- **Logs**: Check application logs for errors

---

## Maintenance

### Updating This File

This CLAUDE.md file should be updated when:

- Project structure changes significantly
- New conventions are adopted
- Development workflow changes
- New tools or frameworks are introduced
- Common issues and solutions are discovered

Keep this file:
- **Current**: Update within a week of changes
- **Accurate**: Verify information is correct
- **Concise**: Focus on what AI assistants need to know
- **Actionable**: Provide clear guidance and examples

### Version History

Track major updates to this file:

- **2025-11-14**: Initial version created
- [Date]: [Brief description of changes]

---

## Additional Resources

- [Project README](./README.md)
- [API Documentation](./docs/api.md)
- [Architecture Decisions](./docs/adr/)
- [Contributing Guidelines](./CONTRIBUTING.md)
- [Code of Conduct](./CODE_OF_CONDUCT.md)

---

*This file is maintained for AI assistants like Claude Code to effectively understand and contribute to this codebase. Keep it updated as the project evolves.*
