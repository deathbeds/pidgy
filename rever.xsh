$PROJECT = 'pidgin'
$ACTIVITIES = 'version_bump changelog tag ghrelease'.split()

$VERSION_BUMP_PATTERNS = [
                         ('setup.py', 'version\s*=.*,', "version='$VERSION',")
                         ]
#$CHANGELOG_FILENAME = 'CHANGELOG.rst'  # Filename for the changelog
#$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'  # Filename for the news template
$PUSH_TAG_REMOTE = 'git@github.com:deathbeds/pidgin.git'

$GITHUB_ORG = 'deathbeds'
$GITHUB_REPO = 'pidgin'
