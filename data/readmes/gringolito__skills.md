# skills

[![skills.sh](https://skills.sh/b/gringolito/skills)](https://skills.sh/gringolito/skills)

AI skills for common tasks — a collection of reusable skills for AI agents that provide procedural knowledge to help them accomplish specific tasks more effectively.

## Installation

Install all skills from this repository using the [skills.sh](https://skills.sh) CLI:

```sh
npx skills add gringolito/skills
```

This will install all skills and make them available to your AI agent.

## Skills

| Skill | Description |
| --- | --- |
| [address-pr-reviews](./skills/address-pr-reviews/) | Address review comments on pull requests |
| [ai-attribution](./skills/ai-attribution/) | Mark issues, pull requests, comments, reviews, and commits written on the user's behalf with a footnote naming the AI model that wrote them |
| [capture-ui-evidence](./skills/capture-ui-evidence/) | Show reviewers UI changes with screenshots or recordings attached to the pull request or review reply |
| [code-review](./skills/code-review/) | Review a change against the project's standards and spec, check that its tests would catch regressions, and return the findings |
| [craft-pr](./skills/craft-pr/) | Craft the current work into a clean, reviewable pull request without changing its behavior |
| [implement-issue](./skills/implement-issue/) | Take a single issue through implementation, PR, CI, and code review until the PR is merged |
| [implement-spec](./skills/implement-spec/) | Implement every sub-issue of a specification by running `implement-issue` on each in dependency order |
| [review-pr](./skills/review-pr/) | Review a pull request with `code-review` and post the findings on it as a review |
| [scope-completeness-review](./skills/scope-completeness-review/) | Check that a parent or spec issue's scope is fully built in the code, and close the issue once it is |
| [writing-skills](./skills/writing-skills/) | Write or edit skills and other instructions meant for agents to follow |

## Review workflow

`code-review` returns actionable findings without publishing them. Each axis summary stays under
200 words; finding details retain the evidence needed to act on them. `review-pr` publishes those
findings as a comment-only pull request review.

Before opening a pull request, `implement-issue` reviews the complete implementation, including
committed branch work and staged, unstaged, or untracked implementation files. It fixes agreed
findings and explains declined findings with brief technical reasons in the pull request description.

## License

[MIT](./LICENSE)
