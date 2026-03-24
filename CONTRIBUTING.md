# Contributing to SIMDCCO

## Development Setup

1. Fork the repository
2. Clone your fork
3. Follow README.md for local setup
4. Create a feature branch: `git checkout -b feature/your-feature`
5. Make your changes
6. Test thoroughly
7. Commit with clear messages
8. Push and create a Pull Request

## Code Standards

### Python (Backend)
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Write tests for new features

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow React best practices
- Component names: PascalCase
- Utilities: camelCase

### Database
- Always create migrations for schema changes
- Never commit .env files
- Use UUID for primary keys

## Security

- Never commit secrets
- Always hash sensitive data
- Follow LGPD guidelines
- Log security events

## Testing

- Write tests for new features
- Maintain >80% code coverage
- Test edge cases
- Manual testing required for UI changes

## Pull Request Process

1. Update README.md if needed
2. Update documentation
3. Link related issues
4. Request review from maintainers
5. Address feedback
6. Merge after approval

## Questions?

Open an issue or contact: dev@simdcco.com.br
