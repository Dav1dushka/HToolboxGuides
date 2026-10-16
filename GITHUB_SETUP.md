# Repository maintenance

Repository: [Dav1dushka/HToolboxGuides](https://github.com/Dav1dushka/HToolboxGuides)

## Folder map

```text
HToolboxGuides/
├── README.md
├── comparison_cheat_sheet.md
├── GITHUB_SETUP.md
├── LICENSE
├── .gitignore
├── blog/
│   └── the-hackers-toolkit.md
└── examples/
    └── local_http_demo.py
```

## Local validation

Run the safe demo:

```bash
python3 examples/local_http_demo.py
```

It binds only to loopback address `127.0.0.1`. No external target is contacted.

## Make changes

1. Edit the Markdown or Python file.
2. Run the local demo and inspect the diff.
3. Commit with a descriptive message.
4. Keep examples fictional and confined to systems you own or are authorized to test.
