# Memory Purge Loop (purgeLoop.sh)

Automated memory management for macOS with intelligent monitoring and safe purging thresholds.

## Usage

```bash
purgeLoop.sh [interval_minutes] [min_ram_percent] [inactive_percent]
```

### Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `interval_minutes` | Optional | Check interval in minutes | 15 |
| `min_ram_percent` | Optional | Min free RAM % before purge | 5 |
| `inactive_percent` | Optional | Min inactive RAM % required | 15 |

## Safety Features
- **Intelligent Thresholds**: Only purges when beneficial
- **Continuous Monitoring**: Regular memory status checks
- **Safe Defaults**: Conservative settings prevent system issues
- **Manual Override**: Ctrl+C to stop monitoring

## Examples

```bash
# Use defaults (15min intervals, 5% RAM, 15% inactive)
./purgeLoop.sh

# Check every 30 minutes
./purgeLoop.sh 30

# Aggressive settings (10min, 3% RAM, 20% inactive)
./purgeLoop.sh 10 3 20

# Conservative settings (60min, 2% RAM, 25% inactive)
./purgeLoop.sh 60 2 25
```

## How It Works

1. **Memory Monitoring**: Continuously checks RAM usage
2. **Threshold Evaluation**: Compares against configured limits
3. **Benefit Analysis**: Only purges when inactive RAM is high enough
4. **Safe Purging**: Uses macOS `purge` command when beneficial
5. **Status Reporting**: Shows before/after memory statistics

## Use Cases
- **Long-Running Systems**: Servers and workstations
- **Memory-Intensive Work**: Video editing, 3D rendering
- **Background Maintenance**: Automated system optimization

## See Also
- [System Functions](../lib/system_functions.md) - Memory management utilities
- [System Administration Overview](../overview.md#system-administration) - Related tools

---

*Script Location: `bash/system/purgeLoop.sh`*  
*Author: Alexander Kucera / babylondreams.de*