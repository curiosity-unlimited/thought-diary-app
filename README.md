# Thought Diary App
- An AI-powered, full-stack web application that allows users to write [Thought Diaries](https://positivepsychology.com/thought-diary/), which help identify & challenge negative thinking patterns, promoting healthier mental habits.

## Getting Started
1. Fork the Repository on GitHub
    1. Go to the repository: https://github.com/curiosity-unlimited/thought-diary-app
    2. Click the "Fork" button in the top-right corner
    3. GitHub will create a copy under your account: https://github.com/YOUR-USERNAME/thought-diary-app

2. Clone the repository from YOUR fork (not the original):
    ```bash
    # Clone YOUR fork (not the original)
    git clone https://github.com/YOUR-USERNAME/thought-diary-app
    cd thought-diary-app
    ```

3. Fetch all branches and tags so that you can see both the initial code and the instructor's implementation:
    ```bash
    git fetch origin --tags
    ```

4. Check all branches and make sure `demo` is in the list:
    ```bash
    git branch -a
    ```

5. Make sure you're on the `main` branch:
    ```bash
    git checkout main
    ```

6. Create a new branch, `develop` for example, for your own work:
    ```bash
    git checkout -b develop
    ```

7. Create feature branches from that branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```

8. Merge feature branches to `develop`:
    ```bash
    # Via GitHub PR or locally:
    git checkout develop
    git merge feature/your-feature-name
    ```

9. To compare your progress with the instructor's:
    ```bash
    # Compare with a specific milestone
    git diff tag-name..your-branch-name
    # See all differences between your work and the reference
    git diff demo..your-branch-name
    ```

10. For a more comprehensive guide, please follow instructions in [`CONTRIBUTING.md`](./CONTRIBUTING.md)

## License

[MIT](LICENSE)